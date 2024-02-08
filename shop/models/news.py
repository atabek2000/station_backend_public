from django.db import models
from common.models.mixins import InfoMixin

class News(InfoMixin):
    ACTIVE_CHOICES = [
        ('1', 'Да'),
        ('0', 'Нет'),
    ]
    TEXT_BOTTOM_CHOICES = [
        ('1', 'Да'),
        ('0', 'Нет'),
    ]
    title = models.CharField('Загаловок',)
    text = models.TextField('Текст')
    link = models.TextField('Ссылка на страницу', default='/catalog')
    image = models.ImageField('Фото',  upload_to='news_image')
    active = models.CharField('Активно', choices=ACTIVE_CHOICES, max_length=1, default='1')
    text_bottom = models.CharField('Текст снизу', choices=TEXT_BOTTOM_CHOICES, max_length=1, default='1')


    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('title',)

    def __str__(self):
        return self.title