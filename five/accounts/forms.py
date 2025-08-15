from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def check_mail(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists")
            return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ('first_name', 'last_name', 'position', 'gender', 'bio')
