from django.db import models
from company.utils.utils import company_image_path
from user.models import MyUser


class Company(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owner', verbose_name='Владелец')
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to=company_image_path, verbose_name='Изображение')
    discounts = models.PositiveIntegerField(verbose_name='Скидки')
    description = models.TextField(verbose_name='Описание')
    instagram = models.URLField(blank=True, null=True, verbose_name='Instagram')
    facebook = models.URLField(blank=True, null=True, verbose_name='Facebook')
    whatsapp = models.URLField(blank=True, null=True, verbose_name='WhatsApp')
    website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт')

    class Meta:
        db_table = 'company'
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return f'Компания {self.name}'


class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    title = models.CharField(max_length=50, unique=True, verbose_name='Название')
    value = models.CharField(max_length=250, verbose_name='Значение')

    class Meta:
        db_table = 'contact'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'Контакт {self.title}'


class WorkSchedule(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='work_schedule',
                                   verbose_name='Компания')
    MONDAY = 'Понедельник'
    TUESDAY = 'Вторник'
    WEDNESDAY = 'Среда'
    THURSDAY = 'Четверг'
    FRIDAY = 'Пятница'
    SATURDAY = 'Суббота'
    SUNDAY = 'Воскресенье'
    DAY_CHOICES = [
        (MONDAY, 'Понедельник'),
        (TUESDAY, 'Вторник'),
        (WEDNESDAY, 'Среда'),
        (THURSDAY, 'Четверг'),
        (FRIDAY, 'Пятница'),
        (SATURDAY, 'Суббота'),
        (SUNDAY, 'Воскресенье'),
    ]
    monday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Понедельника')
    monday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Понедельника')
    tuesday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Вторника')
    tuesday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Вторника')
    wednesday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Среды')
    wednesday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Среды')
    thursday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Четверга')
    thursday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Четверга')
    friday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Пятницы')
    friday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Пятницы')
    saturday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Субботы')
    saturday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Субботы')
    sunday_start = models.TimeField(null=True, blank=True, verbose_name='Начало Воскресенья')
    sunday_end = models.TimeField(null=True, blank=True, verbose_name='Конец Воскресенья')

    class Meta:
        verbose_name = 'Рабочее время'
        verbose_name_plural = 'Рабочее время'

    def __str__(self):
        return f'Рабочее время для {self.company}'
