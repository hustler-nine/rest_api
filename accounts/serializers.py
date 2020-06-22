from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('age',)


class UserSerializer(serializers.ModelSerializer):
    profile_user = ProfileUserSerializer(source='profile')
    online = serializers.ReadOnlyField(source='profile.online')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'profile_user', 'online',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user_profile = Profile.objects.create(
            user=user,
            age=profile_data['age']
        )
        user.save()
        return user
