from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import TaskForm
from .models import Task


# TASK VIEWS
class HomePageView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homepage')


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner

    def get_success_url(self):
        return reverse_lazy('homepage')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.owner

    def get_success_url(self):
        return reverse_lazy('homepage')


def like_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.is_authenticated:
        if request.user in task.likes.all():
            task.likes.remove(request.user)
        else:
            task.likes.add(request.user)
    return redirect('homepage')
