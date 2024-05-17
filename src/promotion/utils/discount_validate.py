from rest_framework.exceptions import ValidationError


def validate_discount(discount):
    if discount > 100:
        raise ValidationError({'message': 'Скидка не может быть больше 100 процентов'})