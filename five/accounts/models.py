from django.db import models
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
        
    def mark_used(self):
        self.is_used = True
        self.save()

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

POSITION_CHOICES = (
    ('M', 'Manager'),
    ('S', 'Supervisor'),
    ('H', 'HR'),
    ('SE', 'Senior Employee'),
    ('JE', 'Junior Employee'),
)


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)    
    position = models.CharField(max_length=2, choices=POSITION_CHOICES, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField(default='this is bio', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


# Connect the signals
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)