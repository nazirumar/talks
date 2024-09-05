from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('private_chat/<str:username>/', views.private_chat, name='private_chat'),
    path('group_chat/<str:room_name>/', views.group_chat, name='group_chat'),
]
