from django.contrib.auth.models import AbstractUser, _user_has_perm
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from users.models.managers import CustomUserManager

class User(AbstractUser):
    username = models.CharField(
        'Никнейм', max_length=255, unique=True, null=True
    )
    email = models.EmailField(
        'Почта', unique=True, null=True, blank=True
    )
    phone_number = PhoneNumberField(
        'Телефон', unique=True, blank=True, null=True
    )

    CUSTOMER_CHOICES = [
        ('retailer', 'Розница'),
        ('wholesale', 'Оптовик'),
    ]
    customer_type = models.CharField(
        'Тип клиента', choices=CUSTOMER_CHOICES, max_length=10, null=True, blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'