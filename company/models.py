import uuid

from django.db import models
from promotion.models import Promotion
# Create your models here.


class Company(models.Model):
    company_id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=75, blank=False, null=True)
    image = models.ImageField(upload_to='company/%Y%m%d/', blank=False)
    description = models.TextField()
    promotions = models.ManyToManyField(Promotion, related_name='companies')


    def __str__(self):
        return self.title




