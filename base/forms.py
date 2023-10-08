from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Room, Message, Topic

class RoomForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=FilteredSelectMultiple('Topics', is_stacked=False),
    )