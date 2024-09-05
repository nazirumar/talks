import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Call, Participant
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        event = text_data_json.get('event')
        sender = self.scope['user']

        if message:
            # Save the chat message asynchronously
            await self.create_chat_message(sender, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username
                }
            )

        if event == 'start_call':
            # Handle start call event asynchronously
            receiver_username = text_data_json['receiver']
            receiver = await self.get_user_by_username(receiver_username)
            call = await self.create_call(sender, receiver)

            await self.add_participant(call, sender)
            await self.add_participant(call, receiver)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_notification',
                    'event': 'incoming_call',
                    'sender': sender.username,
                    'receiver': receiver.username,
                    'room_name': self.room_name
                }
            )

        if event == 'end_call':
            # Handle end call event asynchronously
            await self.end_call()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'call_notification',
                    'event': 'end_call',
                    'sender': sender.username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def call_notification(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_chat_message(self, sender, message):
        return ChatMessage.objects.create(
            room_name=self.room_name,
            sender=sender,
            message=message
        )

    @database_sync_to_async
    def get_user_by_username(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def create_call(self, caller, receiver):
        return Call.objects.create(
            caller=caller,
            receiver=receiver,
            room_name=self.room_name
        )

    @database_sync_to_async
    def add_participant(self, call, user):
        return Participant.objects.create(
            call=call,
            user=user
        )

    @database_sync_to_async
    def end_call(self):
        call = Call.objects.get(room_name=self.room_name, is_active=True)
        call.is_active = False
        call.save()
        return call
