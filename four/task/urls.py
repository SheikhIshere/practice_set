from django.urls import path
from .views import HomePageView, TaskCreateView, TaskUpdateView, TaskDeleteView, like_task

app_name = 'task'

urlpatterns = [
    # path('', HomePageView.as_view(), name='homepage'),
    path('task/add/', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/like/', like_task, name='task_like'),

]
