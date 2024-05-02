from django.db import models

from promotion.models import Promotion
from user.models import MyUser


class Review(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='author', verbose_name="Автор")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='promotion', verbose_name="Акция")
    body = models.TextField(verbose_name="Текст отзыва")
    likes = models.ManyToManyField(MyUser, related_name='likes', blank=True, verbose_name="Лайки")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        ordering = ['-created_time']
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        username = self.author.username
        return f'Отзыв от {username if username else self.author.email}'
