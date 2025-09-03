from django.contrib.auth.models import User
from django import forms
from .models import ProfileModel
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user = super().save(commit=False)
        if commit:
            user.save()
        
        default_avatar = 'images/default_avatar.png'  # Path relative to the 'static' directory

        profile = ProfileModel.objects.create(
            user = user,
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            phone = self.cleaned_data['phone'],
            address = self.cleaned_data['address'],
            gender = default_avatar
        )

        return profile
