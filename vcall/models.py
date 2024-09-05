from django.contrib.auth.models import User
from django.db import models
import uuid

class Call(models.Model):
    STATUS_CHOICES = [
        ('ringing', 'Ringing'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    caller = models.ForeignKey(User, related_name='calls_made', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='calls_received', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ringing')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.caller.username} -> {self.receiver.username} ({self.room_name})'

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="participants")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in call {self.call.room_name}"

class Invitation(models.Model):
    invite_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="invitations")
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations_received")
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations_sent")
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation {self.invite_id} for call {self.call.room_name} from {self.inviter.username} to {self.invitee.username}"

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} in {self.room_name}: {self.message[:50]}'
