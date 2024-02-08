from django.db import models

from common.models.mixins import DateMixin


# Create your models here.


class Subscribe(DateMixin):
    email = models.EmailField('Почта', )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('email',)

    def __str__(self):
        return self.email