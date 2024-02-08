import uuid

from _decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models.functions import datetime

from shop.models.products import Product
from users.models.users import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Payment(models.Model):
    RESULT_CHOICES = [
        ('0', 'Неудача'),
        ('1', 'Успех'),
    ]
    METHOD_CHOICES = [
        ('wallet', 'Электронные деньги'),
        ('internetbank', 'Интернет-банкинг'),
        ('other', 'Терминалы'),
        ('bankcard', 'Банковские карты'),
        ('cash', 'Точки приема платежей'),
        ('mobile_commerce', 'Мобильная коммерция'),
    ]
    pg_amount = models.DecimalField('Стоимость', max_digits=20, decimal_places=2)
    created_time = models.DateTimeField('Время оплаты', default=datetime.datetime.now, editable=False)
    pg_order_id = models.CharField('Идентификатор заказа')
    pg_payment_id = models.CharField('Идентификатор в системе FreedomPay')
    pg_ps_amount = models.DecimalField('Полная сумма (в валюте которой был произведен платеж)', blank=True, null=True, max_digits=20, decimal_places=2)
    pg_ps_full_amount = models.DecimalField('Полная сумма (в валюте которой был произведен платеж)', blank=True, null=True, max_digits=20, decimal_places=2)
    pg_ps_currency = models.CharField('Валюта, в которой был произведен платеж',blank=True, null=True)
    pg_description = models.TextField('Описание платежа',blank=True, null=True)
    pg_user_phone = models.CharField('Телефон покупателя',blank=True, null=True)
    pg_user_contact_email = models.CharField('Email покупателя',blank=True, null=True)
    pg_payment_method = models.CharField('Метод платежа',blank=True, null=True, choices=METHOD_CHOICES, default='internetbank')
    pg_card_brand = models.CharField('Код бренда карты',blank=True, null=True)
    pg_result = models.CharField('Результат платежа', choices=RESULT_CHOICES)

    def __str__(self):
        return f'{self.pg_payment_id} - {self.pg_amount} - {self.pg_result}'

    class Meta:
        verbose_name = 'Оплата заказа'
        verbose_name_plural = 'Оплаты заказа'
        ordering = ('-created_time',)


class Order(models.Model):
    STATUS_WAITING_PAYMENT = 'waiting_payment'
    STATUS_ERROR = 'error'
    STATUS_PAID = 'paid'
    STATUS_CHOICES = [
        (STATUS_WAITING_PAYMENT, 'Ожидание оплаты'),
        (STATUS_ERROR, 'Ошибка'),
        (STATUS_PAID, 'Оплачено')
    ]

    DELIVERY_CHOICES = [
        ('self', 'Самовызов'),
        ('yandex', 'Яндекс доставка'),
        ('in_country', 'Доставка по стране'),
        ('inter_national', 'Международная доставка'),
        # ('ups', 'UPS'),
    ]
    order_number = models.UUIDField('Номер заказа',default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField('Статус заказа', max_length=32, choices=STATUS_CHOICES, default=STATUS_WAITING_PAYMENT)
    amount = models.DecimalField('Стоимость', max_digits=20, decimal_places=2, blank=True, null=True)
    created_time = models.DateTimeField('Создано',auto_now_add=True, editable=False)
    comment = models.TextField('Комментарии',blank=True, null=True)
    country = models.TextField("Страна",blank=True, null=True)
    city = models.TextField("Город",blank=True, null=True)
    delivery = models.CharField('Доставка', choices=DELIVERY_CHOICES,blank=True, null=True)
    street = models.TextField('Улица',blank=True, null=True)
    house = models.CharField('Дом',max_length=255,blank=True, null=True)
    office = models.CharField('Кв/офис',max_length=255,blank=True, null=True)
    intercom = models.CharField('Домофон',max_length=255,blank=True, null=True)
    entrance = models.CharField('Подъезд',max_length=255,blank=True, null=True)
    floor = models.CharField('Этаж',max_length=255,blank=True, null=True)

    payment = models.OneToOneField(
        to=Payment, on_delete=models.PROTECT, related_name='orders', verbose_name='Оплата', blank=True, null=True
    )

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_time',)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Заказ'
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.PROTECT, related_name='order_items', verbose_name='Товар'
    )
    quantity = models.DecimalField('Количество', max_digits=10, decimal_places=2, default=1)
    price = models.DecimalField('Цена', max_digits=20, decimal_places=2)
    discount = models.DecimalField('Акция', max_digits=20, decimal_places=2,default=0, blank=True)

    def __str__(self):
        return f'{self.product} - {self.quantity} - {self.price}'

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'
        ordering = ('order',)

    @property
    def amount(self):
        return self.quantity * (self.price - self.discount)




# class Review(models.Model):
#     user = models.ForeignKey(
#         to=User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь'
#     )
#     product = models.ForeignKey(
#         to=Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар'
#     )
#     rating = models.IntegerField('Оценка',default=5, validators=[
#             MaxValueValidator(100),
#             MinValueValidator(1)
#     ])
#     message = models.TextField('Отзыв')
#
#     def __str__(self):
#         return f'{self.product} - {self.rating} '
#
#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'