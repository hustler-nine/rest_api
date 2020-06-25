from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=queryset)
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=queryset)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message', 'timestamp',)
