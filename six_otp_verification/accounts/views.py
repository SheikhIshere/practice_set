from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProfileModel

# Create your views here.


class SignupView(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')

class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class ProfileVeiw(TemplateView, LoginRequiredMixin):
    template_name = 'profile.html'

