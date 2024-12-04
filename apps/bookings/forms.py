from django import forms
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
                }
            ),
            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                    'placeholder': 'Any special requirements or notes for the provider?'
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            # Check if start time is in the future
            if start_time < timezone.now():
                raise forms.ValidationError("Start time must be in the future")
            
            # Check if end time is after start time
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time")
            
            # Check if duration is within reasonable limits (e.g., max 8 hours)
            duration = (end_time - start_time).total_seconds() / 3600
            if duration > 8:
                raise forms.ValidationError("Booking duration cannot exceed 8 hours")

        return cleaned_data