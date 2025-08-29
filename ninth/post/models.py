from django.db import models
from accounts.models import User
from django.utils.text import slugify
# Create your models here.


class PostModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    discription = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s post with '{self.title}' title"
    