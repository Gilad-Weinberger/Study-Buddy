from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'about', 'username', 'email', 'avatar', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'avatar']