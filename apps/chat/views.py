from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import ChatRoom, Message
from apps.users.models import CustomUser

class ChatListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/chat_list.html'
    context_object_name = 'chat_rooms'

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants').order_by('-created_at')

class ChatRoomView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat/chat_room.html'
    context_object_name = 'chat_room'
    pk_url_kwarg = 'room_id'

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(
            room=self.object
        ).select_related('sender').order_by('created_at')
        return context

class ChatCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    template_name = 'chat/chat_create.html'
    fields = []

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        other_user = get_object_or_404(CustomUser, id=self.kwargs['user_id'])
        
        # Check if chat room already exists
        existing_room = ChatRoom.objects.filter(
            participants=self.request.user
        ).filter(
            participants=other_user
        ).first()
        
        if existing_room:
            return redirect('chat:room', room_id=existing_room.id)
        
        # Create new chat room
        chat_room = form.save()
        chat_room.participants.add(self.request.user, other_user)
        return super().form_valid(form)