from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='list'),
    path('<int:room_id>/', views.ChatRoomView.as_view(), name='room'),
    path('create/<int:user_id>/', views.ChatCreateView.as_view(), name='create'),
]