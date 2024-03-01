# Generated by Django 4.2.8 on 2024-02-06 11:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import promotion.models
import promotion.utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(null=True, upload_to=promotion.utils.utils.category_image_path)),
                ('icon', models.FileField(null=True, upload_to=promotion.utils.utils.category_icon_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg'])])),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='promotion.promotioncategory')),
            ],
            options={
                'verbose_name': 'promotion_category',
                'verbose_name_plural': 'promotion_categories',
                'db_table': 'promotion_category',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='promotion/%Y-%m-%d/')),
                ('old_price', models.PositiveIntegerField(null=True)),
                ('new_price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(null=True, validators=[promotion.models.validate_discount])),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('Discount', 'Скидка'), ('Bonus', 'Бонус'), ('Certificate', 'Сертификат')], default='Discount', max_length=45)),
                ('contacts', models.CharField(max_length=100)),
                ('work_time', models.CharField(max_length=25, null=True)),
                ('address', models.CharField(max_length=85)),
                ('end_date', models.DateField()),
                ('is_daily', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='promotion.promotioncategory')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
                'db_table': 'promotion',
            },
        ),
    ]
