from django.db import models
from django.core.validators import FileExtensionValidator

from company.models import Company
from user.models import MyUser
from promotion.utils.utils import category_image_path, category_icon_path
from promotion.utils.discount_validate import validate_discount

from phonenumber_field.modelfields import PhoneNumberField


class PromotionCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(upload_to=category_image_path, null=True, verbose_name='Изображение')
    icon = models.FileField(upload_to=category_icon_path, null=True, blank=True,
                            validators=[FileExtensionValidator(allowed_extensions=['svg']),],
                            verbose_name='Иконка')
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='subcategories',
                                        verbose_name='Родительская категория')

    def __str__(self):
        return f'Категория {self.title}'

    class Meta:
        db_table = 'promotion_category'
        verbose_name = 'Категория акции'
        verbose_name_plural = 'Категории акций'


class Promotion(models.Model):
    PROMOTION_CHOICES = (
        ('Discount', 'Скидка'),
        ('Bonus', 'Бонус'),
        ('Certificate', 'Сертификат'),
        ('Draw', 'Розыгрыш'),
    )
    category = models.ForeignKey(PromotionCategory, null=True, blank=True,
                                 on_delete=models.CASCADE, related_name='category',
                                 verbose_name='Категория')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Компания')
    title = models.CharField(max_length=100, verbose_name='Название')
    slider_image = models.ImageField(upload_to='promotion/slides/%Y-%m-%d/',
                                     verbose_name='Изображение для слайдера')
    old_price = models.PositiveIntegerField(null=True, verbose_name='Старая цена')
    new_price = models.PositiveIntegerField(verbose_name='Новая цена')
    discount = models.PositiveIntegerField(null=True, validators=[validate_discount], verbose_name='Скидка')
    description = models.TextField(verbose_name='Описание')
    type = models.CharField(max_length=45, choices=PROMOTION_CHOICES, default=PROMOTION_CHOICES[0][0],
                            verbose_name='Тип')
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес')
    likes = models.ManyToManyField(MyUser, related_name='liked_promotions', blank=True, null=True,
                                   verbose_name='Лайки')
    favorites = models.ManyToManyField(MyUser, related_name='favorite_promotions', blank=True, null=True,
                                       verbose_name='Избранное')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    is_daily = models.BooleanField(default=False, verbose_name='Ежедневно')
    instagram = models.URLField(blank=True, null=True, verbose_name='Instagram')
    facebook = models.URLField(blank=True, null=True, verbose_name='Facebook')
    whatsapp = models.URLField(blank=True, null=True, verbose_name='WhatsApp')
    website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт')
    user = models.ForeignKey(MyUser, related_name='users', blank=True, null=True,
                                verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        if self.category:
            return f'Акция {self.title} с категорией {self.category.title}'
        else:
            return f'Акция {self.title}'

    class Meta:
        db_table = 'promotion'
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class PromotionImage(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    image = models.ImageField(upload_to=category_image_path, null=True, verbose_name='Изображение')
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='images',
                                  verbose_name='Акция')

    def __str__(self):
        return f'Фото для {self.title} '

    class Meta:
        db_table = 'promotion_image'
        verbose_name = 'Изображение акции'
        verbose_name_plural = 'Изображения акций'


class PromotionContact(models.Model):
    phone = PhoneNumberField('Номер телефона')
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='promotion_contact',
        verbose_name='К какой акции относиться'
    )

    def __str__(self) -> str:
        return f'номер: {self.phone}, акция: {self.promotion}'

    class Meta:
        verbose_name = 'Номер телефона'
        verbose_name_plural = verbose_name
