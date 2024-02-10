from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=150, verbose_name='Почта')
    phone = models.IntegerField(verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='user/', verbose_name='Аватар', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='Город', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    last_login = models.DateTimeField(auto_now=True, verbose_name='Дата последнего входа', **NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

