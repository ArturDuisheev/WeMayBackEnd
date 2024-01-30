from rest_framework import serializers
from promotion.models import PromotionCategory, Promotion, Like


class PromotionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionCategory
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Promotion
        fields = ['category', 'title', 'image', 'old_price', 'discount', 'description', 'type', 'contacts', 'work_time', 'address', 'likes']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'promotion']
