from django.db import models
from django.contrib.auth.models import User

Category = (
    ('Personal', 'Personal'),
    ('Work', 'Work'),
    ('Study', 'Study'),
    ('Family', 'Family'),
    ('Health', 'Health'),
    ('Finance', 'Finance'),
    ('Shopping', 'Shopping'),
    ('Travel', 'Travel'),
    ('Entertainment', 'Entertainment'),
    ('Hobbies', 'Hobbies'),
    ('Sports', 'Sports'),
    ('Others', 'Others'),
)

class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='This task does not have a description yet.')
    category = models.CharField(max_length=20, choices=Category, default='Others')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dead_line = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    def increase_likes(self):
        self.likes.add(self.user)
        self.save()
    
