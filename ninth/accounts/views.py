from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import *


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        # login(user, self.request)
        login(self.request, user) 
        return redirect('accounts:profile', username=user.username)

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})



class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ProfileModel.objects.get_or_create(user = self.object)
        context['profile'] = profile
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ProfileModel
    form_class = UpdateProfileForm
    template_name = 'profile_update.html'

    def get_object(self, *args, **kwargs):
        profile,created = ProfileModel.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})
        


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset/password_reset.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset/password_reset_complete.html'
