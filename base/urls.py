from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('topics/', views.all_topics, name='all_topics'),
    path('room/<int:room_id>/', views.room, name='room'),
]