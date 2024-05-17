from django_filters import rest_framework as filters

from promotion import models as prom_mod

from django.utils import timezone


class CustomPromotionFilter(filters.FilterSet):
    min_discount = filters.NumberFilter(field_name='discount', lookup_expr='gte')
    popular = filters.OrderingFilter(
        fields=(
            ('likes', 'likes'),
        ),
        label='Popular',
        method='order_by_likes'
    )
    highest_price = filters.OrderingFilter(
        fields=(
            ('new_price', 'new_price'),
        ),
        label='Highest Price',
        method='order_by_highest_price'
    )
    lowest_price = filters.OrderingFilter(
        fields=(
            ('new_price', 'new_price'),
        ),
        label='Lowest Price',
        method='order_by_lowest_price'
    )
    new = filters.BooleanFilter(
        method='filter_new'
    )

    def order_by_likes(self, queryset, name, value):
        return queryset.order_by('-likes')

    def order_by_highest_price(self, queryset, name, value):
        return queryset.order_by('-new_price')

    def order_by_lowest_price(self, queryset, name, value):
        return queryset.order_by('new_price')

    def filter_new(self, queryset, name, value):
        if value:
            two_days_ago = timezone.now() - timezone.timedelta(days=2)
            return queryset.filter(created_at__gte=two_days_ago)
        return queryset

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
