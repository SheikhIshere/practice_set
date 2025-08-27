from django.contrib.auth import login
from django.views.generic import DetailView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import SignUpform
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ProfileModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import ProfileUpdateForm
# Create your views here.


class SignupView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpform

    def form_valid(self, form):
        user = form.save()
        # Create a profile for the new user with default values
        ProfileModel.objects.create(
            user=user,
            mobile='',  # You might want to add this to your form
            bio=''      # You might want to add this to your form
        )
        login(self.request, user)
        return redirect('accounts:profile', username=user.username)


class SigninView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class ProfileView(DetailView):
    template_name = 'profile.html'
    model = User  # The model to use to get the object
    slug_field = 'username'  # The field to use as the slug in the URL
    slug_url_kwarg = 'username'  # The name of the URL parameter that captures the slug value

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])
        # This method is called to get the object that will be used to populate the template context.
        # In this case, we're getting the user object based on the 'username' URL parameter.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ProfileModel.objects.get_or_create(user=self.object)
        context['profile'] = profile  # Add the profile object to the template context
        return context
    



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = ProfileModel
    form_class = ProfileUpdateForm
    template_name = "profile_update.html"


    def get_object(self, queryset=None):
        return get_object_or_404(ProfileModel, user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={
            'username': self.request.user.username
        })