# Generated by Django 4.2.8 on 2024-01-29 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0005_alter_promotion_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]