from django.db import models

from common.functions.cyrillic_to_latin import cyrillic_to_latin
from common.models.mixins import InfoMixin


class Brand(InfoMixin):
    SHOW_CHOICE = [
        ('0', 'Нет'),
        ('1', 'Да'),
    ]
    name = models.CharField('Название', max_length=255)
    show_on_main = models.CharField('Показать на главной странице?', choices=SHOW_CHOICE, default='0')
    show_on_main_order = models.IntegerField('Порядок на главной(чем больше, тем выше)', default=0)
    image = models.ImageField('Лого', upload_to='brand_image', blank=True, null=True)
    slug = models.SlugField(blank=True, default='slug')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = cyrillic_to_latin(self.name)
        super().save(*args, **kwargs)
