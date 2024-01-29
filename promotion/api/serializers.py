from rest_framework import serializers
from promotion.models import PromotionCategory, Promotion


class PromotionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCategory
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["category"] = instance.category.title
        return representation

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Promotion.likes.model
#         fields = ['id', 'user', 'promotion']
#         fields = '__all__'
