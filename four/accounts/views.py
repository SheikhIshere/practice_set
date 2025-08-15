from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth.models import User


# AUTH VIEWS
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile', username=user.username)


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


# PROFILE
class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        context['profile'] = self.object.profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_edit.html'

    def get_object(self):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})
