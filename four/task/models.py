from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('urgent', 'Urgent'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='work')
    is_done = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
