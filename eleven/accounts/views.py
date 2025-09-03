from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .forms import SignupForm, LoginForm, OTPVerificationForm, ProfileForm
from .models import Profile, OTP
from .utils import generate_and_send_otp_for_user, verify_user_otp, can_resend_otp
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

User = get_user_model()  # define once at the top of views.py


# Helper keys stored in session
SESSION_OTP_USER_ID = 'otp_user_id'
SESSION_OTP_PURPOSE = 'otp_purpose'

def signup_view(request):
    """
    Create a new User account (email not verified yet) and send signup OTP.
    After successful form save, an OTP is sent and the user is redirected to verify page.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ensure profile exists (signal)
            profile = user.profile
            # send OTP
            generate_and_send_otp_for_user(user, purpose='signup_verification')
            # store in session so verification knows which user/purpose
            request.session[SESSION_OTP_USER_ID] = user.id
            request.session[SESSION_OTP_PURPOSE] = 'signup_verification'
            messages.success(request, "Account created. A verification code was sent to your email.")
            return redirect('accounts:verify_email')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """
    Authenticate credentials then generate login 2FA OTP (no session created yet).
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                # send login 2FA OTP
                generate_and_send_otp_for_user(user, purpose='login_2fa')
                request.session[SESSION_OTP_USER_ID] = user.id
                request.session[SESSION_OTP_PURPOSE] = 'login_2fa'
                messages.info(request, "A login code was sent to your email. Enter it to complete login.")
                return redirect('accounts:verify_login_otp')
            else:
                # Generic error - do not leak whether username/email exists
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('accounts:login')



def verify_email_view(request):
    """
    Verify OTP after signup. On success mark profile.email_verified=True, log the user in.
    """
    user_id = request.session.get(SESSION_OTP_USER_ID)
    purpose = request.session.get(SESSION_OTP_PURPOSE)

    if not user_id or purpose != 'signup_verification':
        messages.error(request, "No signup verification process found.")
        return redirect('accounts:login')

    # ✅ get actual user object
    user = get_object_or_404(User, pk=user_id)
    profile = user.profile

    # compute resend cooldown seconds
    can_resend, seconds_left = can_resend_otp(user, 'signup_verification')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            ok, msg = verify_user_otp(user, 'signup_verification', code)
            if ok:
                profile.email_verified = True
                profile.save()
                # log the user in now that email is verified
                login(request, user)
                # clear session keys
                request.session.pop(SESSION_OTP_USER_ID, None)
                request.session.pop(SESSION_OTP_PURPOSE, None)
                messages.success(request, "Email verified and logged in.")
                return redirect('/')
            else:
                messages.error(request, msg)
    else:
        form = OTPVerificationForm()

    return render(
        request,
        'accounts/verify_email.html',
        {'form': form, 'seconds_left': seconds_left}
    )



def verify_login_otp_view(request):
    """
    Verify OTP after initial credential check for login. On success create session via login().
    """
    user_id = request.session.get(SESSION_OTP_USER_ID)
    purpose = request.session.get(SESSION_OTP_PURPOSE)
    if not user_id or purpose != 'login_2fa':
        messages.error(request, "No login verification process found.")
        return redirect('accounts:login')

    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)

    can_resend, seconds_left = can_resend_otp(user, 'login_2fa')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            ok, msg = verify_user_otp(user, 'login_2fa', code)
            if ok:
                # create session for user
                login(request, user)
                # clear session keys
                request.session.pop(SESSION_OTP_USER_ID, None)
                request.session.pop(SESSION_OTP_PURPOSE, None)
                messages.success(request, "Login successful.")
                return redirect('/')
            else:
                messages.error(request, msg)
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/verify_login_otp.html', {'form': form, 'seconds_left': seconds_left})

def resend_otp_view(request):
    """
    Resend OTP for the outstanding session-bound otp process (signup or login).
    Respects per-OTP cooldown.
    """
    user_id = request.session.get(SESSION_OTP_USER_ID)
    purpose = request.session.get(SESSION_OTP_PURPOSE)
    if not user_id or purpose not in ('signup_verification', 'login_2fa'):
        messages.error(request, "No OTP flow in progress.")
        return redirect('accounts:login')

    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)

    allowed, seconds_left = can_resend_otp(user, purpose)
    if not allowed:
        messages.error(request, f"Please wait {seconds_left}s before resending the code.")
    else:
        generate_and_send_otp_for_user(user, purpose)
        messages.success(request, "A new code has been sent to your email.")

    # redirect back to appropriate verification page
    if purpose == 'signup_verification':
        return redirect('accounts:verify_email')
    return redirect('accounts:verify_login_otp')

@login_required
def profile_view(request):
    """Show the user's profile page (read-only)."""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    """Allow user to update name, bio, and profile image."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})
