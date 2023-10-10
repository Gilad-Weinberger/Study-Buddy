from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User  

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email']