from django.db import models

from common.models.mixins import InfoMixin
from common.functions.cyrillic_to_latin import cyrillic_to_latin


class Product(InfoMixin):
    ACTIVE_CHOICES = [
        ('1', 'Да'),
        ('0', 'Нет'),
    ]
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField(blank=True, unique=True, max_length=255)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2,)
    discount = models.DecimalField('Скидка', max_digits=10, decimal_places=2, default=0)
    active = models.CharField('Активно', choices=ACTIVE_CHOICES, max_length=1, default='1')
    GENDER_CHOICES = [
        ('m', 'Мужской'),
        ('f', 'Женский'),
        ('u', 'Унисекс'),
    ]
    gender = models.CharField('Пол', choices=GENDER_CHOICES, max_length=1)
    # on_sale = models.DecimalField('Цена по акции', max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField('Описание', blank=True, null=True)
    views = models.IntegerField('Просмотры', default=0)
    remain = models.DecimalField('Остаток', max_digits=10, decimal_places=2, null=True, blank=True)
    main_image = models.ImageField('Фото', upload_to='product_main_image', blank=True, null=True)

    brand = models.ForeignKey(
        to='shop.Brand', on_delete=models.RESTRICT, related_name='products', verbose_name='Бренд', null=True, blank=True
    )

    size = models.ManyToManyField(
        to='shop.Size', related_name='products', verbose_name='Размеры', blank=True
    )

    type = models.ForeignKey(
        to='shop.ProductType', on_delete=models.RESTRICT, related_name='products', verbose_name='Тип', null=True, blank=True
    )

    size_type = models.ForeignKey(
        to='shop.SizeType', related_name='products', verbose_name='Тип размера', blank=True, null=True, on_delete=models.CASCADE,
        # to='shop.SizeType', related_name='products', verbose_name='Тип размера', blank=True, default=1, on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = cyrillic_to_latin(self.name)
        super().save(*args, **kwargs)
