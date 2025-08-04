from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Only show conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__username']

    def get_queryset(self):
        # Filter to only messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')  # from nested URL
        conversation = Conversation.objects.get(pk=conversation_id)

        # Enforce user must be a participant
        if self.request.user not in conversation.participants.all():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
