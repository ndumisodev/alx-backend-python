from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, source='sender_id')

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj)
        return MessageSerializer(messages, many=True).data
