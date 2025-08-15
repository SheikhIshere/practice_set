# from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from . import forms
from django.shortcuts import redirect


# Homepage view


# User Registration View
class UserRegisterView(CreateView):
    model = User
    form_class = forms.UserRegisterForm  # Your custom form extending UserCreationForm
    template_name = 'signup.html'    

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in user after signup
        print('User authenticated right after login?', self.request.user.is_authenticated)
        return redirect('account:profile')
        
    # def get_success_url(self):
    #     return reverse_lazy('account:profile')


# User Login View
class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('account:profile')


# User Logout View
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('account:login')


# account/views.py
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    login_url = reverse_lazy('account:login')  # Add this line
    
    def get_object(self):
        return self.request.user