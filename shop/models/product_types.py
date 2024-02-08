from django.db import models
from common.models.mixins import InfoMixin


class ProductType(InfoMixin):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Тип товаров'
        verbose_name_plural = 'Типы товаров'
        ordering = ('name',)

    def __str__(self):
        return self.name
