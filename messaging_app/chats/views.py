from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.
    """
    queryset =Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters conversations to only include those where the requesting user
        is a participant.
        """
        user = self.request.user
        # Ensure the user is authenticated before filtering
        if user.is_authenticated:
            # Filter conversations where the current user is a participant
            return Conversation.objects.filter(participants=user).order_by('-created_at')
        return Conversation.objects.none() # Return empty queryset if user is not authenticated

    def perform_create(self, serializer):
        """
        Custom create logic for conversations.
        - Ensures the creator is automatically added as a participant.
        """
        # Save the conversation instance first, which handles participant_ids via the serializer's create()
        instance = serializer.save()
        # Ensure the creator is always a participant of the conversation
        if self.request.user not in instance.participants.all():
            instance.participants.add(self.request.user)
        instance.save() # Save again if participants were added/modified


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    