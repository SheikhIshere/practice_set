from django.shortcuts import get_object_or_404, redirect
from .models import TaskModel
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.views import View

class TaskListView(LoginRequiredMixin, ListView):
    model = TaskModel
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return TaskModel.objects.all().order_by('-created_at')



class AddTaskView(LoginRequiredMixin, CreateView):
    model = TaskModel
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = TaskModel
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task:task_list')

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = TaskModel
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task:task_list')

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = TaskModel
    template_name = 'task_details.html'
    context_object_name = 'task'

    def get_success_url(self):
        return reverse_lazy('task:task_detail', kwargs={'pk': self.get_object().pk})




class LikedTaskView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(TaskModel, pk=pk)
        task.likes.add(request.user)  # add like
        return redirect('task:task_detail', pk=task.pk)

    def get(self, request, pk, *args, **kwargs):
        # allow GET too, in case your link is <a href="...">
        task = get_object_or_404(TaskModel, pk=pk)
        task.likes.add(request.user)
        return redirect('task:task_detail', pk=task.pk)
