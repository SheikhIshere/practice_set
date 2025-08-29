from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(null=True, blank=True)
    bio = models.CharField(max_length=1005, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"