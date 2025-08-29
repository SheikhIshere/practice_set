from django.urls import path
from .views import PostListView, CreatePostView, PostDetailsView, UpdatePostView, DeletePostView

app_name = 'post'

urlpatterns = [
    path('post-list/', PostListView.as_view(), name='post_list'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post-details/<int:pk>/', PostDetailsView.as_view(), name='post_details'),
    path('update-post/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
    path('delete-post/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
]
