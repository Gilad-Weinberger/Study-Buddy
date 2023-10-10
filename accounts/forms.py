from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        