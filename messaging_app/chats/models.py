from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status_message = models.CharField(max_length=255, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

# Conversation Model
class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    topic = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    group_image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.is_group:
            return f"Group: {self.group_name or 'Unnamed Group'}"
        return f"Conversation {self.id} - Participants: {', '.join([user.username for user in self.participants.all()])}"

# Message Model
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages_sent")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('file', 'File'),
            ('audio', 'Audio')
        ],
        default='text'
    )
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

