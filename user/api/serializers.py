from rest_framework import serializers
from user.models import MyUser


class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, write_only=True)
    client_id = serializers.CharField(max_length=200, write_only=True)
    client_secret = serializers.CharField(max_length=200, write_only=True)
    grant_type = serializers.CharField(max_length=200, write_only=True)
    email = serializers.CharField(max_length=100)

    def create(self, validated_data):
        validated_data.pop('client_id')
        validated_data.pop('client_secret')
        validated_data.pop('grant_type')
        user = MyUser.objects.create_user(**validated_data)
        return user
