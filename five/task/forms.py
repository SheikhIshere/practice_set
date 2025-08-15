from django import forms
from .models import TaskModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'category', 'is_completed', 'dead_line']

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'category', 'is_completed', 'dead_line']