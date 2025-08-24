from random import randint
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
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, FormView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from .models import ProfileModel, OTP
from .forms import ProfileUpdateForm, OTPVerificationForm
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




# otp verification

from datetime import datetime, timedelta
from random import randint
from django.core.cache import cache

class OTPMixin:
    OTP_EXPIRY_MINUTES = 5
    
    def generate_otp(self, user):
        """Generate and store a new OTP for the user."""
        otp = str(randint(100000, 999999))
        expires_at = timezone.now() + timezone.timedelta(minutes=self.OTP_EXPIRY_MINUTES)
        
        # Create or update OTP for the user
        otp_obj, created = OTP.objects.update_or_create(
            user=user,
            defaults={
                'otp': otp,
                'expires_at': expires_at,
                'is_used': False
            }
        )
        return otp
    
    def send_otp(self, user, otp):
        """Send OTP to the user (placeholder - implement actual sending logic here)."""
        # In a real app, implement actual email/SMS sending here
        print(f"Sending OTP to {user.email}: {otp}")
        return True
    
    def verify_otp(self, user, otp):
        """Verify if the provided OTP is valid for the user."""
        try:
            otp_obj = OTP.objects.filter(
                user=user,
                otp=otp,
                is_used=False,
                expires_at__gt=timezone.now()
            ).latest('created_at')
            
            otp_obj.mark_used()
            return True, "OTP verified successfully"
            
        except OTP.DoesNotExist:
            return False, "Invalid or expired OTP"


class OTPVerificationView(LoginRequiredMixin, FormView):
    template_name = 'registration/otp_verify.html'
    form_class = OTPVerificationForm
    success_url = reverse_lazy('task:task_list')  # Update with your success URL
    
    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        otp_mixin = OTPMixin()
        success, message = otp_mixin.verify_otp(self.request.user, otp)
        
        if success:
            messages.success(self.request, message)
            # Mark user as verified or perform other actions
            return super().form_valid(form)
        else:
            messages.error(self.request, message)
            return self.form_invalid(form)


class RequestOTPView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/request_otp.html'
    
    def get(self, request, *args, **kwargs):
        otp_mixin = OTPMixin()
        otp = otp_mixin.generate_otp(request.user)
        otp_mixin.send_otp(request.user, otp)
        messages.info(request, 'A new OTP has been sent to your registered email.')
        return redirect('accounts:verify_otp')