from rest_framework import serializers
from .models import User, Conversation, Message
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, source='sender_id')
    message_body = serializers.CharField()
    # queryset = Conversation.objects.prefetch_related('participants', Prefetch('messages', queryset=Message.objects.select_related('sender')))

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or just whitespace.")
        if len(value) < 3:
            raise serializers.ValidationError("Message body must be at least 3 characters.")
        return value
    
    def get_messages(self, obj):
        request = self.context.get('request')
        messages = Message.objects.filter(conversation=obj)
        page = self.paginate_queryset(messages, request)
        serializer = MessageSerializer(page, many=True)
        return serializer.data


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation=obj)
        return MessageSerializer(messages, many=True).data

    read_only_fields = ['user_id', 'created_at'] 
