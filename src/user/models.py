import uuid

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from user.api.managers import MyUserManager
from user.utils.utils import user_image_path, default_user_image_path


class MyUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Идентификатор"
    )
    username = models.CharField(unique=True, max_length=50, null=True, blank=True, verbose_name="Имя пользователя")
    fullname = models.CharField(max_length=200, null=True, blank=True, verbose_name="Полное имя")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    image = models.ImageField(upload_to=user_image_path, default=default_user_image_path, blank=True,
                              verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь", )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname', 'image']

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username if self.username else self.email} uuid: {self.id}'
