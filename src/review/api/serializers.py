from rest_framework import serializers

from core.env_reader import env
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'promotion',
            'body',
            'likes',
            'created_time'
        )

    def get_author(self, obj):
        base_url = env('BASE_URL')
        image_url = None

        if obj.author.image:
            image_url = base_url + obj.author.image.url

        return {
            'username': obj.author.username,
            'image': image_url
        }
