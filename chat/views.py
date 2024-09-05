from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, PrivateChat, Message
from django.contrib.auth import get_user_model

User = get_user_model()




def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/home.html', {'users':users})


@login_required
def chat_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    latest_messages = room.messages.all()

    return render(request, 'chat/room.html', {
        'room': room,
        'latest_messages': latest_messages,
    })

@login_required
def private_chat(request, username):
    user2 = get_object_or_404(User, username=username)
    room = PrivateChat.objects.get_or_create_private_chat(request.user, user2)
    
    return redirect('chat_room', room_name=room.name)

@login_required
def group_chat(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name)
    room.participants.add(request.user)
    
    return redirect('chat_room', room_name=room.name)
