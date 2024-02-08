from django.db import models

from shop.models.products import Product


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='Фотки товара')
    image = models.ImageField(upload_to='product_images')
