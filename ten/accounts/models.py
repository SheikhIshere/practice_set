from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.templatetags.static import static


# Define gender choices
GENDER = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

class ProfileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True, null=True, default='Not Specified')
    last_name = models.CharField(max_length=100, blank=True, null=True, default='Not Specified')
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True, default='01*******')
    address = models.CharField(max_length=100, blank=True, null=True, default='earth')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png')

    gender = models.CharField(max_length=1, choices=GENDER, default='O')

    @property
    def image_url(self):
        if self.avatar and default_storage.exists(self.avatar.name):
            return self.avatar.url
        return static('images/default_avatar.png')

    def __str__(self):
        return f"{self.get_full_name()}'s profile"
