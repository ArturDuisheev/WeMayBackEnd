# Generated by Django 4.2.8 on 2024-02-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0010_rename_old_price_promotion_price_promotion_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_daily',
            field=models.BooleanField(default=False),
        ),
    ]