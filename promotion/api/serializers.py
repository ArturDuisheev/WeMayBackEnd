from rest_framework import serializers
from promotion.models import PromotionCategory, Promotion


class PromotionCategorySerializer(serializers.ModelSerializer):
    promotions_count = serializers.SerializerMethodField()

    class Meta:
        model = PromotionCategory
        fields = ['id', 'title', 'image', 'parent_category', 'promotions_count']

    def get_promotions_count(self, obj):
        return Promotion.objects.filter(category=obj).count()


class PromotionSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Promotion
        fields = ['category', 'title', 'image', 'old_price', 'discount', 'description', 'type', 'contacts', 'work_time', 'address', 'likes']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.title
        return representation
