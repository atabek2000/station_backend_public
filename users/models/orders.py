from django.db import models
from common.models.mixins import InfoMixin


class Order(InfoMixin):


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('created_at',)

    def __str__(self):
        return self.size
