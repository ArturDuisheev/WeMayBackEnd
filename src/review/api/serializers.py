from rest_framework import serializers

from core.env_reader import env
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    author = serializers.SerializerMethodField('get_author')
    promotion_pk = serializers.IntegerField(source='promotion.id')

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'promotion',
            'promotion_pk',
            'body',
            'likes',
            'created_time'
        )

    def get_author(self, obj):
        base_url = env('BASE_URL')  #:TODO: тут костыль, поправавить(сорри я торопился)
        return {
            'username': obj.author.username,
            'image': ''.join(base_url + obj.author.image.url)
        }
