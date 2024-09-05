from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Room(models.Model):
    """
    Model representing a chat room.
    This can be either a private chat (one-to-one) or a group chat (many-to-many).
    """
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_private = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_private:
            return f"Private chat between {', '.join([user.username for user in self.participants.all()])}"
        return self.name if self.name else f"Group chat with {self.participants.count()} participants"


class Message(models.Model):
    """
    Model representing a chat message in a room.
    """
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender} in {self.room} at {self.timestamp}"


class PrivateChatManager(models.Manager):
    """
    Manager to handle the creation of private chats.
    """
    def get_or_create_private_chat(self, user1, user2):
        if user1 == user2:
            raise ValueError("Cannot create a private chat with the same user")
        
        room_name = f"private_{min(user1.id, user2.id)}_{max(user1.id, user2.id)}"
        room, created = Room.objects.get_or_create(
            name=room_name,
            is_private=True
        )
        room.participants.add(user1, user2)
        return room


class PrivateChat(Room):
    """
    Proxy model to represent private chats more specifically.
    """
    objects = PrivateChatManager()

    class Meta:
        proxy = True
        verbose_name = "Private Chat"
        verbose_name_plural = "Private Chats"
