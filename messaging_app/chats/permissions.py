from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to only allow access to users who are participants in the conversation.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()