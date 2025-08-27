from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=15)
    bio = models.TextField()

    def __str__(self):
        return f"{self.user.get_full_name()}'s profile" or "{self.user.username}'s profile"


