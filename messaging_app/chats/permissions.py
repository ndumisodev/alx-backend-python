from rest_framework import permissions

class IsMessageOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a message to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the message
        return obj.sender == request.user or obj.receiver == request.user

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()