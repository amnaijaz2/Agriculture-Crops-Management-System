"""
Template-based views for Authentication.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib import messages
from .forms import RegisterForm


class LoginView(View):
    """Handle user login."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboards:dashboard')
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboards:dashboard')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'authentication/login.html', {'form': form})


class RegisterView(View):
    """Handle user registration."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboards:dashboard')
        form = RegisterForm()
        return render(request, 'authentication/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboards:dashboard')
        return render(request, 'authentication/register.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('authentication:login')
