from django_filters import rest_framework as filters

from promotion import models as prom_mod


class CustomPromotionFilter(filters.FilterSet):
    min_discount = filters.NumberFilter(field_name='discount', lookup_expr='gte')

    class Meta:
        model = prom_mod.Promotion
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'type': ['exact'],
            'address': ['icontains'],
            'category__title': ['exact'],
            'discount': ['exact'],
            'is_daily': ['exact'],
            'company__name': ['exact'],
        }
