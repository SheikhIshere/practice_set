from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.urls import reverse_lazy
# Create your views here.


class SignUpView(CreateView):    
    form_class = SignUpForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return reverse_lazy ('accounts:profile', username=user.username)

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_obj'

    def get_object(self):
        return self.request.user