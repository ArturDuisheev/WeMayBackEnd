# Generated by Django 4.2.8 on 2024-03-21 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotion', '0002_alter_promotion_image_alter_promotion_slider_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
