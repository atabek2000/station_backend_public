from django.db import models
from common.models.mixins import InfoMixin


class SizeType(InfoMixin):
    name = models.CharField('Названия на сайте', max_length=255)
    name_second = models.CharField('Названия на админке', max_length=255, blank=True)

    size_1 = models.CharField(blank=True)
    size_2 = models.CharField(blank=True)
    size_3 = models.CharField(blank=True)
    size_4 = models.CharField(blank=True)
    size_5 = models.CharField(blank=True)
    size_6 = models.CharField(blank=True)
    size_7 = models.CharField(blank=True)
    size_8 = models.CharField(blank=True)
    size_9 = models.CharField(blank=True)
    size_10 = models.CharField(blank=True)
    size_11 = models.CharField(blank=True)
    size_12 = models.CharField(blank=True)
    size_13 = models.CharField(blank=True)
    size_14 = models.CharField(blank=True)
    size_15 = models.CharField(blank=True)
    size_16 = models.CharField(blank=True)
    size_17 = models.CharField(blank=True)
    size_18 = models.CharField(blank=True)
    size_19 = models.CharField(blank=True)
    size_20 = models.CharField(blank=True)
    size_21 = models.CharField(blank=True)
    size_22 = models.CharField(blank=True)
    size_23 = models.CharField(blank=True)
    size_24 = models.CharField(blank=True)
    size_25 = models.CharField(blank=True)
    size_26 = models.CharField(blank=True)
    size_27 = models.CharField(blank=True)
    size_28 = models.CharField(blank=True)
    size_29 = models.CharField(blank=True)
    size_30 = models.CharField(blank=True)

    class Meta:
        verbose_name = 'Тип размера'
        verbose_name_plural = 'Типы размера'
        ordering = ('name',)

    def __str__(self):
        return self.name_second

    def save(self, *args, **kwargs):
        if self.name_second == '':
            self.name_second = self.name
        super().save(*args, **kwargs)
