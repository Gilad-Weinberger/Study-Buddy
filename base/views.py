from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Topic, Message
from .forms import CreateRoomForm
from django.utils import timezone
from django.db import models
from django.db.models import Q, Max, OuterRef, Subquery
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        rooms = Room.objects.all()

    current_time = timezone.now()
    last_hour = current_time - timezone.timedelta(hours=1)

    for room in rooms:
        room.user_connected_recently = room.host.last_login >= last_hour

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


def room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    messages = room.get_messages_ordered_by_datetime()

    messages_list = list(messages)
    previous_message_date = None  
    for message in messages_list:
        message_date = message.date_sent.date()
        message.new_day = message_date != previous_message_date   
        previous_message_date = message_date

    subquery = Message.objects.filter(user=OuterRef('id'), room=room).order_by('-date_sent')
    
    participants = room.participants.exclude(id=room.user_created.id).annotate(
        last_message_date=Subquery(subquery.values('date_sent')[:1])
    )

    if request.method == 'POST':
        text = request.POST.get('text')
        code = request.POST.get('code')

        code = code if code.strip() != '' else None

        texts = text.strip()
        if texts != '':
            message = Message.objects.create(
                room=room,
                user=request.user,
                text=text,
                code=code,
                date_sent=timezone.now()
            )
            message.save()
            return redirect('room', room_id=room.id)

    user_in_room = False

    if request.user.is_authenticated:
        is_in_group = room.participants.filter(id=request.user.id).exists()
        if is_in_group:
            user_in_room = True

    participants_list = list(participants)
    for participant in participants_list:
        participant.full_name = f"{participant.first_name} {participant.last_name}"

    room.user_created.full_name = f"{room.user_created.first_name} {room.user_created.last_name}"

    context = {
        'room': room,
        'messages': messages,
        'user_in_room': user_in_room,
        'participants': participants,
    }

    return render(request, 'base/room.html', context)

@login_required
def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)  
            room.user_created = request.user  
            room.date_created = timezone.now()  
            room.save()  
            room.participants.add(request.user)

            messages.success(request, 'Room created successfully!')
            return redirect('room', room_id=room.id)
    else:
        form = CreateRoomForm()

    context = {'form': form}

    return render(request, 'base/create_room.html', context)

@login_required
def join_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.user in room.participants.all():
        return redirect('room', room_id=room.id)

    room.participants.add(request.user)
    return redirect('room', room_id=room.id)

@login_required
def leave_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.user in room.participants.all():
        room.participants.remove(request.user)

    return redirect('home')