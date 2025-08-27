from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}" or f"profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
    else:
        instance.profile.save()        




# # this is just testing
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         ProfileModel.objects.create(user=instance)


# def save_user_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):
#         instance.profile.save()


# # Connect the signals
# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)