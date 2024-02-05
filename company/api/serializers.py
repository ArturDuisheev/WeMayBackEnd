from rest_framework import serializers
from company.models import Company, Contact


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company_name'] = instance.company.name
        return representation
