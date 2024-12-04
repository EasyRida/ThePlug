from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Booking
from .forms import BookingForm
from apps.skills.models import Skill
from apps.reviews.forms import ReviewForm

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(
            renter=user
        ).select_related('skill', 'provider').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_bookings'] = self.get_queryset().filter(
            status__in=['pending', 'confirmed']
        )
        context['past_bookings'] = self.get_queryset().filter(
            status__in=['completed', 'cancelled']
        )
        return context

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.select_related('skill', 'provider', 'renter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = self.get_object()
        
        if booking.can_be_reviewed():
            context['review_form'] = ReviewForm()
            
        return context

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_id = self.kwargs.get('skill_id')
        context['skill'] = get_object_or_404(Skill, id=skill_id)
        return context

    @transaction.atomic
    def form_valid(self, form):
        skill_id = self.kwargs.get('skill_id')
        skill = get_object_or_404(Skill, id=skill_id)
        
        form.instance.skill = skill
        form.instance.provider = skill.provider
        form.instance.renter = self.request.user
        
        # Calculate total amount based on hourly rate and duration
        duration = (form.instance.end_time - form.instance.start_time).total_seconds() / 3600
        form.instance.total_amount = skill.hourly_rate * duration
        
        messages.success(self.request, 'Booking created successfully! Please proceed to payment.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payments:create', kwargs={'booking_id': self.object.id})

class BookingCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, id=pk, renter=request.user)
        
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
        
        return redirect('bookings:detail', pk=booking.id)

class BookingCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, id=pk, provider=request.user)
        
        if booking.status == 'confirmed':
            booking.status = 'completed'
            booking.save()
            messages.success(request, 'Booking marked as completed.')
        else:
            messages.error(request, 'This booking cannot be marked as completed.')
        
        return redirect('bookings:detail', pk=booking.id)