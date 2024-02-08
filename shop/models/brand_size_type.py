from django.db import models
from common.models.mixins import InfoMixin


class BrandSizeType(InfoMixin):
    MAIN_CHOICES = [
        ('1', 'Да'),
        ('0', 'Нет'),
    ]
    main = models.CharField('Главный', choices=MAIN_CHOICES, max_length=1, default='0')

    brand = models.ForeignKey(
        to='shop.Brand', on_delete=models.RESTRICT, related_name='brand_size_types', verbose_name='Бренд', null=True, blank=True
    )

    product_type = models.ForeignKey(
        to='shop.ProductType', on_delete=models.RESTRICT, related_name='brand_size_types', verbose_name='Тип товара', null=True,
        blank=True
    )

    size_type = models.ForeignKey(
        to='shop.SizeType', on_delete=models.RESTRICT, related_name='brand_size_types', verbose_name='Тип размера', null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Бренд для тип размера'
        verbose_name_plural = 'Бренды для тип размера'
        ordering = ('-main',)

    def __str__(self):
        return f'{self.brand} - {self.product_type}'
