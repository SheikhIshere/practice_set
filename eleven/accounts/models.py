from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    """Profile linked one-to-one with the default User, storing OTP and email-verification info."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=150, blank=True)   # display name
    bio = models.TextField(blank=True)                    # user bio
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)  # profile picture


    email_verified = models.BooleanField(default=False)
    otp_hash = models.CharField(max_length=128, null=True, blank=True)
    otp_salt = models.CharField(max_length=32, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    OTP_PURPOSE_CHOICES = [
        ('signup', 'Signup Verification'),
        ('login', 'Login 2FA'),
    ]
    otp_purpose = models.CharField(max_length=10, choices=OTP_PURPOSE_CHOICES, null=True, blank=True)
    otp_resend_available_at = models.DateTimeField(null=True, blank=True)
    failed_otp_attempts = models.IntegerField(default=0)
    otp_locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# Signal to create or update Profile whenever a User is created.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('signup', 'Signup Verification'),
        ('login', 'Login 2FA'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_hash = models.CharField(max_length=128)
    otp_salt = models.CharField(max_length=32)
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    resend_available_at = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_locked(self):
        return self.locked_until and self.locked_until > timezone.now()


    def __str__(self):
        return f"OTP for {self.user.username} ({self.purpose})"



