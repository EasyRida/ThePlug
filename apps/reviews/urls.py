from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:booking_id>/', views.ReviewCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ReviewUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete'),
]