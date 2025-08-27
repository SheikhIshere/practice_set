from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
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
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class ProfileView(DetailView):
    template_name = 'profile.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        try:
            return User.objects.select_related('profilemodel').get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        try:
            context['profile'] = user.profilemodel
        except ProfileModel.DoesNotExist:
            context['profile'] = ProfileModel.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                mobile=''
            )
        return context
    
    
    
    