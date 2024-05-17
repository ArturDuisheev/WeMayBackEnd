from .models import Promotion


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

