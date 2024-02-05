from django.db import models
from company.utils.utils import company_image_path


class Company(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=company_image_path)
    discounts = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'company'
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return f'Компания {self.name}'


class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return f'Контакт {self.title}'
