from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants of a conversation to view, update, delete messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - obj: Message or Conversation
        - request.user must be one of the participants of obj.conversation
        """
        if hasattr(obj, 'participants'):
            # obj is a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is a Message
            return request.user in obj.conversation.participants.all()
        return False
