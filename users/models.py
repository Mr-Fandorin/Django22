from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Телефон", help_text="Введите номер телефона")
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name="Аватар")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна", help_text="Укажите вашу страну")

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
