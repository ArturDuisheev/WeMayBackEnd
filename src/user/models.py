from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from user.api.managers import MyUserManager
from user.utils.utils import user_image_path, default_user_image_path


class MyUser(AbstractUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50, null=True, blank=True)
    fullname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=user_image_path, default=default_user_image_path, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname', 'image']

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(("pbkdf2_sha256$", "bcrypt")):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'Пользователь {self.username if self.username else self.email}'
