from django.db import models
from user.models import MyUser


class PromotionCategory(models.Model):
    title = models.CharField(max_length=30)
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='subcategories')

    class Meta:
        db_table = 'promotion_category'
        verbose_name = 'promotion_category'
        verbose_name_plural = 'promotion_categories'


class Promotion(models.Model):
    PROMOTION_CHOICES = (
        ('Discount', 'Скидка'),
        ('Bonus', 'Бонус'),
        ('Certificate', 'Сертификат')
    )
    category = models.ForeignKey(PromotionCategory, null=True, blank=True,
                                 on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=25)
    image = models.ImageField(upload_to='promotion/%Y%m%d/')
    old_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True)
    description = models.TextField()
    type = models.CharField(max_length=45, choices=PROMOTION_CHOICES, default=PROMOTION_CHOICES[0][0])
    contacts = models.CharField(max_length=45)
    work_time = models.CharField(max_length=25, null=True)
    address = models.CharField(max_length=85)
    likes = models.ManyToManyField(MyUser, related_name='liked_promotions')
    # created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promotion'
        verbose_name = 'promotion'
        verbose_name_plural = 'promotions'
