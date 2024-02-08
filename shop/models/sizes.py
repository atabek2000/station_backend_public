from django.db import models
from common.models.mixins import InfoMixin


class Size(InfoMixin):
    size = models.CharField('Размер', max_length=255)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ('size',)

    def __str__(self):
        return self.size
