# Generated by Django 4.2.8 on 2024-02-04 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0004_alter_promotion_type'),
        ('company', '0004_remove_company_promotion_company_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='promotion.promotion'),
        ),
    ]
