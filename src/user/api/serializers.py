from rest_framework import serializers
from user.models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    client_id = serializers.CharField(max_length=200, write_only=True)
    client_secret = serializers.CharField(max_length=200, write_only=True)
    grant_type = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'client_secret', 'client_id', 'grant_type']

    def create(self, validated_data):
        validated_data.pop('client_id')
        validated_data.pop('client_secret')
        validated_data.pop('grant_type')
        user = MyUser.objects.create_user(**validated_data)
        return user
