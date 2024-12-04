from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': 'you@example.com'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': 'John'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': 'Doe'
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': '+27 123 456 789'
        })
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': 'City, Country'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': '••••••••'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'location', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'location', 'bio', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm'
            })
        }