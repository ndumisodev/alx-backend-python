from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation for any action:
    - View (GET)
    - Update (PUT/PATCH)
    - Delete (DELETE)
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - obj can be a Message or Conversation
        """
        user = request.user

        # If obj is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If obj is a Message
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation

            # Explicitly check for each HTTP method
            if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                return user in conversation.participants.all()

        return False
