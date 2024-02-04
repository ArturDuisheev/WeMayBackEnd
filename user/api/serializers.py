from rest_framework import serializers
from user.models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user
