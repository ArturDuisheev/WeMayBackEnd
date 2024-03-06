from rest_framework import serializers
from promotion.models import PromotionCategory, Promotion
from review.models import Review


class PromotionCategorySerializer(serializers.ModelSerializer):
    promotions_count = serializers.SerializerMethodField()

    class Meta:
        model = PromotionCategory
        fields = ['id', 'title', 'image', 'parent_category', 'promotions_count', 'icon']

    def get_promotions_count(self, obj):
        return Promotion.objects.filter(category=obj).count()


class PromotionSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['category', 'company', 'title', 'image',
                  'old_price', 'new_price', 'discount',
                  'description', 'type', 'contacts',
                  'work_time', 'address', 'likes', 'images',
                  'end_date', 'is_daily', 'reviews_count']

    def get_reviews_count(self, obj):
        return Review.objects.filter(promotion=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_name'] = instance.category.title
        return representation
