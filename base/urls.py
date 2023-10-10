from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('topics/', views.all_topics, name='all_topics'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('join_room/<int:room_id>/', views.join_room, name='join_room'),
]