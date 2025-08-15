from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from .forms import UserRegistraionForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

class UserRegistraionView(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = UserRegistraionForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile')

class UserLoginView(LoginView):
    template_name = 'login.html'    

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

class UserLogOutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class UserProfileView(LoginRequiredMixin, DetailView):
    # model = User this basicly no need
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    login_url = reverse_lazy('accounts:login')

    def get_object(self):
        return self.request.user