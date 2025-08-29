from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import PostModel
from .forms import PostForm, EditPostForm

class PostListView(ListView):
    model = PostModel
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

class CreatePostView(LoginRequiredMixin, CreateView):
    model = PostModel
    form_class = PostForm
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post:post_list')

class PostDetailsView(DetailView):
    model = PostModel
    template_name = 'post_details.html'
    context_object_name = 'post'

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PostModel
    form_class = EditPostForm
    template_name = 'update_post.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

    def get_success_url(self):
        return reverse_lazy('post:post_details', kwargs={'pk': self.object.pk})

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PostModel
    template_name = 'confirm_delete_post.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

    def get_success_url(self):
        return reverse_lazy('post:post_list')
