from rest_framework import serializers

from user.models import MyUser


class AuthUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    password = serializers.CharField(max_length=60)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'username']


class CustomUserSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()
    email = serializers.EmailField(required=False)

    class Meta:
        model = MyUser
        fields = ['id', 'email', 'username', 'fullname', 'image']
