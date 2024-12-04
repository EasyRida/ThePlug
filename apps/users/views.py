from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.db.models import Avg, Count, Sum, F, ExpressionWrapper, fields
from django.db.models.functions import ExtractHour
from django.views.generic import TemplateView, UpdateView
from .forms import SignUpForm, UserProfileForm
from .models import CustomUser
from apps.bookings.models import Booking
from apps.skills.models import Skill

@method_decorator(ensure_csrf_cookie, name='dispatch')
class SignUpView(View):
    template_name = 'users/signup.html'
    form_class = SignUpForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = request.POST.get('user_type', 'client')
            user.username = user.email  # Set username to email
            user.save()
            
            # Authenticate and login the user
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.email, password=raw_password)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Account created successfully!')
                
                if user.user_type == 'provider':
                    return redirect('users:provider_dashboard')
                return redirect('users:client_dashboard')
            
        return render(request, self.template_name, {'form': form})

# ... rest of the views remain the same ...