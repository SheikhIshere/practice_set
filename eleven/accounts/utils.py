import os
import base64
import hashlib
import hmac
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import OTP

# Security params
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 5
RESEND_COOLDOWN_SECONDS = 60
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 10


def _generate_numeric_otp(length=OTP_LENGTH):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def _hash_otp(otp, salt=None):
    """
    Hash otp with a salt and return (salt, hash_hex).
    Salt: base64-encoded random bytes.
    """
    if salt is None:
        salt = base64.b64encode(os.urandom(6)).decode()
    h = hashlib.sha256((salt + otp).encode()).hexdigest()
    return salt, h


def generate_and_send_otp_for_user(user, purpose):
    """
    Generate an OTP, store hashed form in OTP model, and send email via Django email.
    Old OTPs for same purpose are invalidated.
    """
    # Invalidate previous OTPs for this user & purpose
    OTP.objects.filter(user=user, purpose=purpose).update(expires_at=timezone.now())

    code = _generate_numeric_otp()
    salt, hashed = _hash_otp(code)
    now = timezone.now()

    otp_obj = OTP.objects.create(
        user=user,
        otp_hash=hashed,
        otp_salt=salt,
        purpose=purpose,
        created_at=now,
        expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES),   # ✅ FIXED
        resend_available_at=now + timedelta(seconds=RESEND_COOLDOWN_SECONDS),
        failed_attempts=0,
    )

    # Render email templates
    ctx = {'user': user, 'otp': code, 'purpose': dict(OTP.PURPOSE_CHOICES).get(purpose, '')}
    subject = "Your verification code"
    text = render_to_string("emails/otp_email.txt", ctx)
    html = render_to_string("emails/otp_email.html", ctx)

    send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html)
    return code


def verify_user_otp(user, purpose, code):
    """
    Verify the latest OTP for the user+purpose.
    Returns (True, message) on success, or (False, message) on failure.
    """
    now = timezone.now()
    otp_obj = OTP.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()

    if not otp_obj:
        return False, "No OTP request found. Please request a new code."

    # Lock check
    if otp_obj.is_locked():
        return False, "Too many attempts. Try again later."

    # Expiry
    if otp_obj.is_expired():
        return False, "Code expired. Request a new one."

    # Hash incoming code with stored salt
    test_hash = hashlib.sha256((otp_obj.otp_salt + code).encode()).hexdigest()
    if not hmac.compare_digest(test_hash, otp_obj.otp_hash):
        otp_obj.failed_attempts += 1
        if otp_obj.failed_attempts >= MAX_FAILED_ATTEMPTS:
            otp_obj.locked_until = now + timedelta(minutes=LOCKOUT_MINUTES)
        otp_obj.save()
        return False, "Invalid code."

    # Success
    otp_obj.expires_at = now  # ✅ mark as used by expiring it
    otp_obj.save()
    return True, "OTP verified."


def can_resend_otp(user, purpose):
    """
    Returns (True, seconds_left) indicating whether user can resend.
    If False, seconds_left is seconds until resend available.
    """
    otp_obj = OTP.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()
    if not otp_obj:
        return True, 0
    now = timezone.now()
    if otp_obj.resend_available_at and otp_obj.resend_available_at > now:
        return False, int((otp_obj.resend_available_at - now).total_seconds())
    return True, 0
