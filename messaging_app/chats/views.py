from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    UserSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations with nested messages
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only conversations where current user is a participant
        """
        return self.queryset.filter(participants=self.request.user).prefetch_related(
            'participants',
            'messages'
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Custom action to add participant to conversation
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response(
                {'status': 'participant added'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a conversation
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages by conversation ID from URL and ensure user is participant
        """
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.filter(
            id=conversation_id,
            participants=self.request.user
        ).first()
        
        if not conversation:
            return Message.objects.none()
            
        return self.queryset.filter(
            conversation=conversation
        ).select_related('sender').order_by('sent_at')

    def perform_create(self, serializer):
        """
        Automatically set sender and conversation when creating message
        """
        conversation = Conversation.objects.filter(
            id=self.kwargs.get('conversation_pk'),
            participants=self.request.user
        ).first()
        
        if not conversation:
            return Response(
                {'error': 'Conversation not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer.save(
            sender=self.request.user,
            conversation=conversation
        )