from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import *
from .models import ProfileModel
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile', username=user.username)


class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={
            'username': self.request.user.username
        })


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(ProfileModel, user=self.object)
        context['profile'] = profile
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ProfileModel
    form_class = ProfileUpdateForm
    template_name = "profile_update.html"


    def get_object(self, queryset=None):
        return get_object_or_404(ProfileModel, user=self.request.user)

        # profile, created = ProfileModel.objects.get_or_create(user=self.request.user)
        # return profile
    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={
            'username': self.request.user.username
        })