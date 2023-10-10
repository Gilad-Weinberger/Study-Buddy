from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Room, Message, Topic
from accounts.models import User

class RoomForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=FilteredSelectMultiple('Topics', is_stacked=False),
    )
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple('User', is_stacked=False),
    )

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']