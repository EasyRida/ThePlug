from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='list'),
    path('create/<int:skill_id>/', views.BookingCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<int:pk>/cancel/', views.BookingCancelView.as_view(), name='cancel'),
    path('<int:pk>/complete/', views.BookingCompleteView.as_view(), name='complete'),
]