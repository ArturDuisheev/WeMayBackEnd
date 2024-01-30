from django.db import models
from company.utils.utils import company_image_path
from promotion.models import Promotion


class Company(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=company_image_path)
    discounts = models.PositiveIntegerField()
    promotions = models.ManyToManyField(Promotion, related_name='promotions')

    class Meta:
        db_table = 'company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'
