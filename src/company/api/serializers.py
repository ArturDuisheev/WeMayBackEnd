from rest_framework import serializers
from company.models import Company, Contact, WorkSchedule
from promotion.models import Promotion


class CompanySerializer(serializers.ModelSerializer):
    promotions_count = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField(method_name='get_category_name')

    class Meta:
        model = Company
        fields = '__all__'

    def get_promotions_count(self, obj):
        return Promotion.objects.filter(company=obj).count()

    def get_category_name(self, obj):
        return obj.category.title if None else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner_username'] = instance.owner.username
        return representation


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company_name'] = instance.company.name
        return representation


class WorkScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkSchedule
        fields = (
            '__all__'
        )
