from rest_framework import serializers

from user.models import MyUser


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(required=False)
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'fullname', 'image']
