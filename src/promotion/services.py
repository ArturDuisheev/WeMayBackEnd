from datetime import date, timedelta
from django.db.models import Count
from .models import Promotion


def get_filtered_promotions(request, filter=None):
    queryset = Promotion.objects.annotate(Count('likes')).order_by('-likes__count')
    filter_dict = {
        'free': queryset.filter(new_price=0),
        'daily': queryset.filter(is_daily=True),
        'end_soon': queryset.filter(
            end_date__lte=date.today() + timedelta(days=3),
            end_date__gte=date.today()
        ),
    }
    return filter_dict.get(filter) if filter in filter_dict else queryset


def get_count(promotion_id, field):
    promotion = Promotion.objects.filter(pk=promotion_id).first()
    if not promotion:
        return None
    return getattr(promotion, field).count()


def toggle_status(promotion_id, user, field, add_message, remove_message):
    promotion = Promotion.objects.filter(pk=promotion_id).first()
    if not promotion:
        return False, 'Акция не найдена'

    field_instance = getattr(promotion, field)
    if user in field_instance.all():
        field_instance.remove(user)
        return True, remove_message
    else:
        field_instance.add(user)
        return True, add_message


def get_like_count(promotion_id):
    return get_count(promotion_id, 'likes')


def toggle_like_status(promotion_id, user):
    return toggle_status(promotion_id, user, 'likes', 'Добавлено в \'Понравившиеся акции\'', 'Лайк удален')


def get_favorite_count(promotion_id):
    return get_count(promotion_id, 'favorites')


def toggle_favorite_status(promotion_id, user):
    return toggle_status(promotion_id, user, 'favorites', 'Добавлено в избранные', 'Удалено из избранных')
