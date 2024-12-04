from django import forms
from django.forms.widgets import FileInput
from .models import Skill, SkillImage, SkillUnavailability

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = [
            'category', 'title', 'description', 'hourly_rate', 
            'location', 'is_remote', 'available_from', 'available_to',
            'available_days', 'min_hours', 'max_hours'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'min': 0,
                'step': 0.01,
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                'placeholder': 'City, Country or Remote'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                'placeholder': 'Enter the title of your skill'
            }),
            'is_remote': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-indigo-600'
            }),
            'available_from': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'available_to': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'available_days': forms.SelectMultiple(attrs={
                'class': 'form-multiselect mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }, choices=[
                (1, 'Monday'),
                (2, 'Tuesday'),
                (3, 'Wednesday'),
                (4, 'Thursday'),
                (5, 'Friday'),
                (6, 'Saturday'),
                (7, 'Sunday'),
            ]),
            'min_hours': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'max_hours': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get('available_from')
        available_to = cleaned_data.get('available_to')
        min_hours = cleaned_data.get('min_hours')
        max_hours = cleaned_data.get('max_hours')

        if available_from and available_to and available_from >= available_to:
            raise forms.ValidationError("Available from time must be before available to time")

        if min_hours and max_hours and min_hours > max_hours:
            raise forms.ValidationError("Minimum hours cannot be greater than maximum hours")

        return cleaned_data

class SkillImageForm(forms.ModelForm):
    class Meta:
        model = SkillImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                'accept': 'image/*'
            })
        }