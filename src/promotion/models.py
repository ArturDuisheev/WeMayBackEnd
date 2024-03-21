from django.db import models
from django.core.validators import FileExtensionValidator

from rest_framework.exceptions import ValidationError

from company.models import Company
from user.models import MyUser
from promotion.utils.utils import category_image_path, category_icon_path

from phonenumber_field.modelfields import PhoneNumberField


def validate_discount(discount):
    if discount > 100:
        raise ValidationError({'message': 'Скидка не может быть больше 100 процентов'})


class PromotionCategory(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=category_image_path, null=True)
    icon = models.FileField(upload_to=category_icon_path, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['svg'])])
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='subcategories')
    
    def __str__(self):
        return f'Категория {self.title}'

    class Meta:
        db_table = 'promotion_category'
        verbose_name = 'promotion_category'
        verbose_name_plural = 'promotion_categories'


class PromotionAddress(models.Model):
    street = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f'{self.street}'

    
class Contact(models.Model):
    phone_number = PhoneNumberField()


class Promotion(models.Model):
    PROMOTION_CHOICES = (
        ('Discount', 'Скидка'),
        ('Bonus', 'Бонус'),
        ('Certificate', 'Сертификат'),
        ('Розыгрыш', 'Розыгрыш')
    )
    category = models.ForeignKey(PromotionCategory, null=True, blank=True,
                                 on_delete=models.CASCADE, related_name='category')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='promotion/%Y-%m-%d/', blank=True, null=True)
    old_price = models.PositiveIntegerField(null=True)
    new_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True, validators=[validate_discount])
    description = models.TextField()
    type = models.CharField(max_length=45, choices=PROMOTION_CHOICES, default=PROMOTION_CHOICES[0][0])
    contacts = models.ManyToManyField(
        Contact,
        verbose_name="Контакты акций",
        related_name='promotion_contacts',
        null=True,
        blank=True,
    )
    work_time = models.CharField(max_length=100, null=True)
    address = models.ManyToManyField(PromotionAddress, related_name='promotions_address')
    likes = models.ManyToManyField(MyUser, related_name='liked_promotions', blank=True, null=True)
    end_date = models.DateField()
    is_daily = models.BooleanField(default=False)

    def __str__(self):
        return f'Акция {self.title} с категорией {self.category.title}'

    class Meta:
        db_table = 'promotion'
        verbose_name = 'promotion'
        verbose_name_plural = 'promotions'





    
