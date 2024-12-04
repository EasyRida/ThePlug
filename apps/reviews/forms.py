from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                'min': '1',
                'max': '5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm',
                'rows': '4'
            })
        }
        help_texts = {
            'rating': 'Rate from 1 to 5 stars',
            'comment': 'Share your experience with this service provider'
        }