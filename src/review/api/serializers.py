from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_username'] = instance.author.username
        representation['promotion_title'] = instance.promotion.title
        return representation
