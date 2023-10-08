from django.db.models import Count
from django.shortcuts import render
from .models import Room, Topic, Message
from django.utils import timezone
from django.db.models import Q  

def Home(request):
    selected_topic = request.GET.get('topic')
    search_query = request.GET.get('search')  

    all_rooms_count = Room.objects.aggregate(total_count=Count('id'))['total_count']

    all_topics = sorted(Topic.objects.all(), key=lambda topic: -topic.total_room_count())
    pop_topics = all_topics[:5]
    recent_messages = Message.objects.order_by('-date_sent')[:3]

    if selected_topic:
        if selected_topic == "All":
            rooms = Room.objects.all()
        else:
            rooms = Room.objects.filter(topics__name=selected_topic)
    else:
        rooms = Room.objects.filter(topics__name=selected_topic)

    current_time = timezone.now()
    last_hour = current_time - timezone.timedelta(hours=1)

    for room in rooms:
        room.user_connected_recently = room.user_created.last_login >= last_hour

    for message in recent_messages:
        message.user_connected_recently = message.user.last_login >= last_hour

    if search_query:
        rooms = rooms.filter(Q(name__icontains=search_query) | Q(user_created__first_name__icontains=search_query))

    context = {
        'all_topics': all_topics,
        'pop_topics': pop_topics,
        'recent_messages': recent_messages,
        'rooms': rooms,
        'all_rooms_count': all_rooms_count,
    }

    return render(request, 'base/home.html', context)

def all_topics(request):
    search_query = request.GET.get('search')

    top_topics = sorted(Topic.objects.all(), key=lambda topic: -topic.total_room_count())[:5]
    all_rooms_count = Room.objects.aggregate(total_count=Count('id'))['total_count']

    if search_query:
        top_topics = sorted(Topic.objects.filter(name__icontains=search_query), key=lambda topic: -topic.total_room_count())[:5]

    context = {
        'top_topics': top_topics,
        'all_rooms_count': all_rooms_count,
    }

    return render(request, 'base/all_topics.html', context)