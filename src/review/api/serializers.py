from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()
    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Review
        fields = (
            'author',
            'promotion',
            'body',
            'likes',
            'created_time'
        )

    def get_author(self, obj):
        request = self.context.get('request')
        image = obj.author.image
        return {
            'username': obj.author.username,
            'image': request.build_absolute_uri(image)
        }




    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['author_username'] = instance.author.username
    #     representation['promotion_title'] = instance.promotion.title
    #     return representation
