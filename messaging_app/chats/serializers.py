from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'bio', 'status_message', 'is_online', 'last_seen', 'location']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Includes nested user data

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'is_read', 'is_deleted']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Includes nested participants' data
    messages = MessageSerializer(many=True, read_only=True, source='messages')  # Includes nested messages within the conversation

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'topic', 'is_group', 'group_name', 'group_image', 'created_at', 'updated_at', 'last_message', 'messages']
