from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with password handling
    """
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']



class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with sender details
    """
    sender = UserSerializer(read_only=tuple, source="sender_id")

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body"]



class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True, many=True)
    messages = MessageSerializer(read_only=True, many=True, source='message_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']