from rest_framework import serializers
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    created_time = serializers.ReadOnlyField()

    class Meta:
        model = Review
        exclude = ['likes']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username
        return representation
