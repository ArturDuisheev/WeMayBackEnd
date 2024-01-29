from django.db import models
from user.models import MyUser
# Create your models here.


class Review(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='author')
    body = models.TextField()
    likes = models.ManyToManyField(MyUser, related_name='likes')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_time']
        db_table = 'review'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
