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
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = '__all__' + 'reviews_count'

    def get_reviews_count(self, obj):
        return Promotion.objects.filter(category=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_name'] = instance.category.title
        return representation
