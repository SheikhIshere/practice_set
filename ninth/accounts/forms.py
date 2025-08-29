from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.', required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class UpdateProfileForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ('first_name', 'last_name', 'mobile', 'bio')
    
def __init__(self, *args, **kwargs):
    """ Initializes the form with the user's current data
    if the form is bound to an instance. """
    super().__init__(*args, **kwargs)
    if self.isinstance and self.instance.user:
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email            
        self.fields['bio'].initial = self.instance.user.bio            
        self.fields['mobile'].initial = self.instance.user.mobile            
    
def save(self, commit=True):
    profile = super().save(commit=False)
    user = profile.user

    user.email = self.cleaned_data['email']
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.bio = self.cleaned_data['bio']
    user.mobile = self.cleaned_data['mobile']

    if commit:
        user.save()
        profile.save()
    return profile


