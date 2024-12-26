from rest_framework import serializers
from .models import CustomUser, Conversation, Message


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)  # Combines first and last name

    class Meta:
        model = CustomUser
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone_number', 'profile_picture', 'bio', 
            'status_message', 'is_online', 'last_seen', 'location'
        ]


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Includes nested user data
    time_sent = serializers.SerializerMethodField()  # Custom field for formatted time

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'conversation', 'message_body', 
            'time_sent', 'is_read', 'is_deleted'
        ]

    def get_time_sent(self, obj):
        """Format the sent_at field as a readable string."""
        return obj.sent_at.strftime('%Y-%m-%d %H:%M:%S') if obj.sent_at else None


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Includes nested participants' data
    messages = MessageSerializer(many=True, read_only=True, source='messages')  # Includes nested messages
    last_message_summary = serializers.SerializerMethodField()  # Custom field for last message preview

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'topic', 'is_group', 
            'group_name', 'group_image', 'created_at', 'updated_at', 
            'last_message', 'last_message_summary', 'messages'
        ]

    def get_last_message_summary(self, obj):
        """Provide a truncated version of the last message."""
        if obj.last_message:
            return obj.last_message[:50] + "..." if len(obj.last_message) > 50 else obj.last_message
        return None
