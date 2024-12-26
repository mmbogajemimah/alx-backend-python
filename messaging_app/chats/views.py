from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages').all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all conversations for the authenticated user.
        """
        user = request.user
        conversations = self.queryset.filter(participants=user)
        serializer = self.serializer_class(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        """
        participants = request.data.get('participants')
        if not participants or not isinstance(participants, list):
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        participants.append(request.user.id)  # Add the requesting user
        conversation = Conversation.objects.create(is_group=request.data.get('is_group', False))
        conversation.participants.set(participants)
        conversation.save()
        serializer = self.serializer_class(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages in a conversation.
    """
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all messages for a specific conversation.
        """
        conversation_id = kwargs.get('conversation_id')
        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        messages = self.queryset.filter(conversation_id=conversation_id)
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation.
        """
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response(
                {"error": "Both conversation ID and message body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.serializer_class(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
