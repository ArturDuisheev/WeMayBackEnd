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

def get_like_count(promotion_id):
    promotion = Promotion.objects.filter(pk=promotion_id).first()
    if not promotion:
        return None
    return promotion.likes.count()

def toggle_like_status(promotion_id, user):
    promotion = Promotion.objects.filter(pk=promotion_id).first()
    if not promotion:
        return False, 'Акция не найдена'

    if user in promotion.likes.all():
        promotion.likes.remove(user)
        return True, 'Лайк удален'
    else:
        promotion.likes.add(user)
        return True, 'Добавлено в \'Понравившиеся акции\''
