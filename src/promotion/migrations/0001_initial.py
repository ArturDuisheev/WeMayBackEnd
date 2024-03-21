# Generated by Django 4.2.8 on 2024-03-21 11:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import promotion.models
import promotion.utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='promotion/%Y-%m-%d/')),
                ('slider_image', models.ImageField(upload_to='promotion/slides/%Y-%m-%d/')),
                ('old_price', models.PositiveIntegerField(null=True)),
                ('new_price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(null=True, validators=[promotion.models.validate_discount])),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('Discount', 'Скидка'), ('Bonus', 'Бонус'), ('Certificate', 'Сертификат'), ('Draw', 'Розыгрыш')], default='Discount', max_length=45)),
                ('work_time', models.CharField(max_length=100, null=True)),
                ('end_date', models.DateField()),
                ('is_daily', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'promotion',
                'verbose_name_plural': 'promotions',
                'db_table': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='PromotionAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PromotionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(null=True, upload_to=promotion.utils.utils.category_image_path)),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='promotion.promotion')),
            ],
            options={
                'verbose_name': 'promotion_image',
                'verbose_name_plural': 'promotion_images',
                'db_table': 'promotion_image',
            },
        ),
        migrations.CreateModel(
            name='PromotionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(null=True, upload_to=promotion.utils.utils.category_image_path)),
                ('icon', models.FileField(null=True, upload_to=promotion.utils.utils.category_icon_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg']), promotion.models.validate_svg_size])),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='promotion.promotioncategory')),
            ],
            options={
                'verbose_name': 'promotion_category',
                'verbose_name_plural': 'promotion_categories',
                'db_table': 'promotion_category',
            },
        ),
        migrations.AddField(
            model_name='promotion',
            name='address',
            field=models.ManyToManyField(related_name='promotions_address', to='promotion.promotionaddress'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='promotion.promotioncategory'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, related_name='promotion_contacts', to='promotion.contact', verbose_name='Контакты акций'),
        ),
    ]
