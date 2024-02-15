# Generated by Django 4.2.8 on 2024-02-06 11:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_promotions', to=settings.AUTH_USER_MODEL),
        ),
    ]