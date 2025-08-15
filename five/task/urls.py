from django.urls import path
from .views import (
    TaskListView,
    AddTaskView,
    EditTaskView,
    DeleteTaskView,
    LikedTaskView,
    TaskDetailView,
)

app_name = 'task'

urlpatterns = [
    path('list/', TaskListView.as_view(), name='task_list'),
    path('add/', AddTaskView.as_view(), name='task_add'),
    path('edit/<int:pk>/', EditTaskView.as_view(), name='task_edit'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='task_delete'),
    path('liked/<int:pk>/' , LikedTaskView.as_view(), name='task_liked'),
    path('task-detail/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),

]
