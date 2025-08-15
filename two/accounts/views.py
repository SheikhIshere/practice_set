from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from django.contrib.auth.models import User

# user signup view
class SignUpView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print('user created successfully == ', user)
        return redirect('accounts:profile')


# user login view
class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    login_url = reverse_lazy('account:login')  # Add this line
    
    def get_object(self):
        return self.request.user