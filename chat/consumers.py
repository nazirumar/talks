import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from chat.models import Message, Room
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def persist_message(self, message):
        # Use sync_to_async to handle the synchronous database operations
        room_instance = await sync_to_async(get_object_or_404)(Room, name=self.room_name)
        await sync_to_async(Message.objects.create)(
            room=room_instance,
            sender=self.user,
            content=message,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )

        # Persist the message
        await self.persist_message(message)

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
