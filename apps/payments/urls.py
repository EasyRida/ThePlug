from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/<int:booking_id>/', views.PaymentCreateView.as_view(), name='create'),
    path('verify/<str:reference>/', views.PaymentVerifyView.as_view(), name='verify'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='cancel'),
    path('webhook/', views.PaystackWebhookView.as_view(), name='webhook'),
]