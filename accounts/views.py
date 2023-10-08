from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User 
from .models import CustomUser
from base.models import Topic, Message, Room
from django.db.models import Count

def user_details(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)  
    rooms_created_by_user = user.rooms_created.all()
    all_rooms_count = Room.objects.aggregate(total_count=Count('id'))['total_count']

    selected_topic = request.GET.get('topic')
    search_query = request.GET.get('search')
    all_topics = sorted(Topic.objects.all(), key=lambda topic: -topic.total_room_count())
    pop_topics = all_topics[:5]
    recent_messages = Message.objects.order_by('-date_sent')[:3]

    if selected_topic:
        rooms = Room.objects.filter(topics__name=selected_topic)
    else:
        rooms = Room.objects.all()

    current_time = timezone.now()
    last_hour = current_time - timezone.timedelta(hours=1)

    for room in rooms:
        room.user_connected_recently = room.user_created.last_login >= last_hour

    for message in recent_messages:
        message.user_connected_recently = message.user.last_login >= last_hour

    if search_query:
        rooms = rooms.filter(Q(name__icontains=search_query) | Q(user_created__first_name__icontains=search_query))

    is_authenticated_user = request.user == user if request.user.is_authenticated else False

    context = {
        'user': user,
        'rooms_created_by_user': rooms_created_by_user,
        'all_rooms_count': all_rooms_count,
        'all_topics': all_topics,
        'pop_topics': pop_topics,
        'recent_messages': recent_messages,
        'is_authenticated_user': is_authenticated_user,
    }

    return render(request, 'accounts/user_details.html', context)

def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'account created successfully')
            return redirect('dashboard-home')
    
    else:
        form = RegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})
