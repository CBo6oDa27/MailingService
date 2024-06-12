from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Введите адрес электронной почты"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="аватар",
        **NULLABLE,
        help_text="Загрузите картинку на аватар"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="номер телефона",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    country = models.CharField(
        max_length=35, verbose_name="страна", **NULLABLE, help_text="Введите страну"
    )
    is_active = models.BooleanField(default=True, verbose_name="активен")
    token = models.CharField(max_length=100, verbose_name="токен", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
