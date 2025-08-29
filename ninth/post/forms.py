from django import forms
from .models import PostModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'discription']


class EditPostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['title', 'discription']

    def save(self, commit=True):
        # Keep the same user when editing
        post = super().save(commit=False)
        if self.instance and self.instance.user:
            post.user = self.instance.user
        if commit:
            post.save()
        return post
