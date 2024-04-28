from django.shortcuts import get_object_or_404
from rest_framework import serializers

from company.models import WorkSchedule
from promotion.models import Promotion, PromotionImage, PromotionCategory, Company, PromotionContact


class WorkScheduleSerializer(serializers.Serializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'


class PromotionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionImage
        fields = '__all__'

class PromotionContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionContact
        fields = '__all__'


class PromotionCategorySerializer(serializers.ModelSerializer):
    count_category = serializers.SerializerMethodField('get_count_category')

    class Meta:
        model = PromotionCategory
        fields = ('title', 'image', 'icon', 'parent_category', 'count_category')

    def get_count_category(self, obj):
        return Promotion.objects.only('category').count()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', ]


class PromotionSerializer(serializers.ModelSerializer):
    company_work_schedule = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    end_date = serializers.DateTimeField(format='%Y-%m-%d T%H:%M:%S')

    class Meta:
        model = Promotion
        fields = ['title', 'image', 'description', 'company', 'company_name', 'category', 'category_name',
                  'type', 'new_price', 'old_price', 'discount', 'address', 'likes', 'end_date',
                  'instagram', 'facebook', 'whatsapp', 'website',
                  'is_daily', 'company_work_schedule']

    def get_company_work_schedule(self, obj):
        if obj.company:
            work_schedule = obj.company.work_schedule
            work_schedule_data = WorkScheduleSerializer(work_schedule).data
            return work_schedule_data

    def create(self, validated_data):
        return Promotion.objects.create(**validated_data)


class MyPromotionSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField('get_like_count')

    class Meta:
        model = Promotion
        fields = (
            'id',
            'image',
            'discount',
            'title',
            'old_price',
            'new_price',
            'likes',
            'like_count',
        )

    def get_like_count(self, obj):
        return obj.likes.count()


class FavoritePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'image',
            'discount',
            'title',
            'old_price',
            'new_price',
            'is_favorite',
        )


class LikeCounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',

        )

class PromotionHintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id',
            'title',
        )
