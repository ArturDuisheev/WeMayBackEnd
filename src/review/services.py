from review.models import Review


def get_count_review(review_id, field):
    review = Review.objects.filter(pk=review_id).first()
    if not review:
        return None
    return getattr(review, field).count()


def toggle_status(review_id, user, field, add_message, remove_message):
    review = Review.objects.filter(pk=review_id).first()

    if not review:
        return False, 'Отзыв не найден'

    if review in getattr(user, field).all():
        getattr(user, field).remove(review)
        return True, remove_message
    else:
        getattr(user, field).add(review)
        return True, add_message


def toggle_like_status(review_id, user):
    return toggle_status(review_id, user, 'likes', 'Лайк добавлен в "Понравившиеся отзывы"',
                         'Отзыв удален из "Понравившиеся отзывы"')


def get_like_count(review_id):
    return get_count_review(review_id, 'likes')
