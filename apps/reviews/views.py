from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Review
from apps.bookings.models import Booking
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = get_object_or_404(Booking, id=self.kwargs['booking_id'])
        return context
    
    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.kwargs['booking_id'])
        if booking.renter != self.request.user:
            messages.error(self.request, "You can only review your own bookings.")
            return redirect('bookings:list')
            
        form.instance.booking = booking
        form.instance.reviewer = self.request.user
        form.instance.reviewee = booking.provider
        messages.success(self.request, "Review submitted successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.kwargs['booking_id']})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    
    def test_func(self):
        review = self.get_object()
        return review.reviewer == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.object.booking.id})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    
    def test_func(self):
        review = self.get_object()
        return review.reviewer == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.object.booking.id})