from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from promotion import models as prom_mod


class CustomPromotionFilter(filters.FilterSet):
    min_discount = filters.NumberFilter(field_name='discount', lookup_expr='gte')

    ordering = filters.OrderingFilter(
        fields=(
            ('likes', 'likes'),
            ('new_price', 'new_price'),
        ),
        field_labels={
            'likes': _('Popular'),
            'new_price': _('Price'),
        }
    )

    new = filters.BooleanFilter(method='filter_new')

    category = filters.BaseInFilter(field_name='category__title', lookup_expr='in', method='filter_by_multiple_values')

    def filter_new(self, queryset, name, value):
        if value:
            two_days_ago = timezone.now() - timezone.timedelta(days=2)
            return queryset.filter(created_at__gte=two_days_ago)
        return queryset

    def filter_by_multiple_values(self, queryset, name, value):
        values = value.split(',')
        return queryset.filter(**{f"{name}__in": values})

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
