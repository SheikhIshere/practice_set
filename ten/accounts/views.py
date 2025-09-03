# from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignUpForm
from django.views.generic import CreateView, DetailView
from .models import ProfileModel
# Create your views here.


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('accounts:profile', username = user.username)

class UserLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in')
        return super(UserLoginView, self).form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super(UserLoginView, self).form_invalid(form)
        
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})



class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ProfileModel.objects.get_or_create(user=self.object)
        context['profile'] = profile
        return context
    
