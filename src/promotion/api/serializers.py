from rest_framework import serializers

from company.models import WorkSchedule
from promotion.models import Promotion, PromotionImage, PromotionCategory, PromotionContact
from user.models import MyUser


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = ('monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
                  'thursday_start', 'thursday_end', 'friday_start', 'friday_end', 'saturday_start', 'saturday_end',
                  'sunday_start', 'sunday_end')


class PromotionContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionContact
        fields = '__all__'


class PromotionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionImage
        fields = '__all__'


class PromotionCategorySerializer(serializers.ModelSerializer):
    count_category = serializers.SerializerMethodField('get_count_category')
    images = PromotionImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = PromotionCategory
        fields = ('title', 'images', 'icon', 'parent_category', 'count_category')

    def get_count_category(self, obj):
        return obj.category.count()


class PromotionSerializer(serializers.ModelSerializer):
    company_work_schedule = serializers.SerializerMethodField(read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    category_name = serializers.CharField(source='category.title', read_only=True)
    end_date = serializers.DateTimeField(format='%Y-%m-%d T%H:%M:%S')
    images = PromotionImageSerializer(many=True, required=False, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all(), many=True, required=False)
    favorites = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all(), many=True, required=False)
    upload_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    promotion_contact = PromotionContactSerializer(read_only=True, many=True)

    class Meta:
        model = Promotion
        fields = ['id', 'title', 'slider_image', 'description', 'company', 'company_name', 'category', 'category_name',
                  'type', 'new_price', 'old_price', 'discount', 'likes', 'favorites', 'end_date',
                  'instagram', 'facebook', 'whatsapp', 'website', 'is_daily', 'company_work_schedule', 'images',
                  'upload_images', 'promotion_contact']

    extra_kwargs = {
        'company': {'required': False}
    }

    def get_company_work_schedule(self, obj):
        if obj.company and hasattr(obj.company, 'work_schedule'):
            work_schedule = obj.company.work_schedule
            work_schedule_data = WorkScheduleSerializer(work_schedule).data
            return work_schedule_data
        return None

    def create(self, validated_data):
        images_data = validated_data.pop('upload_images', [])
        likes_data = validated_data.pop('likes', None)
        favorites_data = validated_data.pop('favorites', None)
        user = validated_data.get('user')

        if Promotion.objects.filter(user=user).exists():
            raise serializers.ValidationError("Акция для этого пользователя уже существует")

        promotion = Promotion.objects.create(**validated_data)

        for image_data in images_data:
            PromotionImage.objects.create(promotion=promotion, image=image_data)

        if likes_data:
            promotion.likes.set(likes_data)

        if favorites_data:
            promotion.favorites.set(favorites_data)

        return promotion


class MyPromotionSerializer(serializers.ModelSerializer):
    images = PromotionImageSerializer(many=True, required=False, read_only=True)
    like_count = serializers.SerializerMethodField('get_like_count')

    class Meta:
        model = Promotion
        fields = (
            'id',
            'images',
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
    images = PromotionImageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Promotion
        fields = (
            'id',
            'images',
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
