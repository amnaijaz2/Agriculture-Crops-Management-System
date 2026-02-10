"""
Template-based views for Users module.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from .forms import UserCreateForm, UserUpdateForm


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to Admin users only."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Display list of all users."""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 15
    ordering = ['-date_joined']


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Create new user."""
    model = User
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Update existing user."""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    context_object_name = 'user_obj'
    success_url = reverse_lazy('users:user_list')


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Delete user."""
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')
    context_object_name = 'user_obj'
