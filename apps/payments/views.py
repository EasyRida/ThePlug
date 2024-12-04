from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
import json
import hmac
import hashlib
import requests
from .models import Payment
from apps.bookings.models import Booking

class PaymentCreateView(LoginRequiredMixin, View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, renter=request.user)
        
        try:
            # Initialize Paystack transaction
            url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'email': request.user.email,
                'amount': int(booking.total_amount * 100),  # Convert to kobo/cents
                'currency': 'ZAR',  # South African Rand
                'callback_url': request.build_absolute_uri(reverse('payments:verify', kwargs={'reference': 'PLACEHOLDER'})),
                'metadata': {
                    'booking_id': booking.id,
                    'custom_fields': [
                        {
                            'display_name': "Skill",
                            'variable_name': "skill",
                            'value': booking.skill.title
                        },
                        {
                            'display_name': "Provider",
                            'variable_name': "provider",
                            'value': booking.provider.get_full_name()
                        }
                    ]
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            
            if response_data['status']:
                # Create payment record
                payment = Payment.objects.create(
                    booking=booking,
                    amount=booking.total_amount,
                    status='pending',
                    paystack_reference=response_data['data']['reference']
                )
                
                return redirect(response_data['data']['authorization_url'])
            else:
                messages.error(request, 'Unable to initialize payment. Please try again.')
                return redirect('bookings:detail', pk=booking_id)
                
        except Exception as e:
            messages.error(request, 'Unable to process payment. Please try again.')
            return redirect('bookings:detail', pk=booking_id)

class PaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request, reference):
        try:
            # Verify Paystack transaction
            url = f'https://api.paystack.co/transaction/verify/{reference}'
            headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
            
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            if response_data['status'] and response_data['data']['status'] == 'success':
                # Update payment status
                payment = get_object_or_404(Payment, paystack_reference=reference)
                payment.status = 'completed'
                payment.save()
                
                # Update booking status
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()
                
                messages.success(request, 'Payment successful!')
                return redirect('payments:success')
            else:
                messages.error(request, 'Payment verification failed.')
                return redirect('payments:cancel')
                
        except Exception as e:
            messages.error(request, 'Payment verification failed.')
            return redirect('payments:cancel')

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/success.html'

class PaymentCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/cancel.html'

@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(View):
    def post(self, request, *args, **kwargs):
        # Verify webhook signature
        paystack_signature = request.headers.get('x-paystack-signature')
        if not paystack_signature:
            return HttpResponse(status=400)

        # Compute expected signature
        computed_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
            request.body,
            hashlib.sha512
        ).hexdigest()

        if paystack_signature != computed_signature:
            return HttpResponse(status=400)

        # Process webhook payload
        payload = json.loads(request.body)
        event = payload['event']

        if event == 'charge.success':
            reference = payload['data']['reference']
            try:
                payment = Payment.objects.get(paystack_reference=reference)
                payment.status = 'completed'
                payment.save()
                
                # Update booking status
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()
                
            except Payment.DoesNotExist:
                return HttpResponse(status=404)

        return HttpResponse(status=200)