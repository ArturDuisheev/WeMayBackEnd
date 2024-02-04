from rest_framework import serializers
from company.models import Company
from promotion.models import Promotion


class CompanySerializer(serializers.ModelSerializer):
    promotion_count = serializers.SerializerMethodField()
    max_discount = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['company_id', 'title', 'image', 'description', 'promotion_count', 'max_discount']

    def get_promotion_count(self, obj):
        return obj.promotions.count()

    def get_max_discount(self, obj):
        max_discount_promotion = obj.promotions.order_by('-discount').first()
        return f'{max_discount_promotion.discount}%' if max_discount_promotion else None


