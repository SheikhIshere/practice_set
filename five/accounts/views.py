from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.contrib.auth import login
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from .models import ProfileModel
from .forms import ProfileUpdateForm
# Create your views here.


# Create a sign up view that inherits from CreateView
class SignUpView(CreateView):    
    form_class = SignUpForm  # Use the SignUpForm for the form
    template_name = 'registration/signup.html'  # Use the signup.html template

    # Override the form_valid method to set the user object and log them in
    def form_valid(self, form):
        user = form.save()  # Save the user object
        login(self.request, user)  # Log the user in
        return redirect ('accounts:profile', username=user.username)  # Redirect to the user's profile

# Create a user login view that inherits from LoginView
class UserLoginView(LoginView):
    template_name = 'registration/login.html'  # Use the login.html template

    # Override the get_success_url method to redirect to the user's profile
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})

# Create a user logout view that inherits from LogoutView
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')  # Redirect to the login page after logout

# Create a profile view that inherits from DetailView
class ProfileView(DetailView):
    model = User  # Use the User model
    template_name = 'registration/profile.html'  # Use the profile.html template
    slug_field = 'username'  # Use the username as the slug field
    slug_url_kwarg = 'username'  # Use the username as the URL keyword argument
    context_object_name = 'profile_user'  # Use the username as the context object name

    # Override the get_object method to get the user object based on the username in the URL
    def get_object(self):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

    # Override the get_context_data method to add the profile to the template context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ProfileModel.objects.get_or_create(user=self.object)
        context['profile'] = profile
        return context


# Create a profile edit view that inherits from UpdateView
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = ProfileModel  # Use the ProfileModel for the model
    template_name = 'registration/profile_edit.html'  # Use the profile_edit.html template
    form_class = ProfileUpdateForm  # Use the ProfileUpdateForm for the form

    # Override the get_object method to get or create the profile if it doesn't exist
    def get_object(self):
        profile, created = ProfileModel.objects.get_or_create(user=self.request.user)
        return profile

    # Override the get_success_url method to redirect to the user's profile
    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    """
    A view that redirects to the user's profile page after login.
    """
    permanent = False
    query_string = True
    pattern_name = 'accounts:profile'

    def get_redirect_url(self, *args, **kwargs):
        """Return the URL to redirect to."""
        kwargs['username'] = self.request.user.username
        return super().get_redirect_url(*args, **kwargs)
