from django.db.models import Max, Min
from rest_framework import serializers
from shop.models import products
from shop.serializers.api.brand import BrandSerializer
from shop.serializers.api.product_type import ProductTypeSerializer
from shop.serializers.api.size import SizeSerializer
from shop.serializers.api.size_type import SizeTypeSerializer
from shop.serializers.nested.product_images import ProductImageSerializer


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    size_type = SizeTypeSerializer(read_only=True)
    type = ProductTypeSerializer(read_only=True)
    brand = BrandSerializer()
    image_path = serializers.SerializerMethodField()

    class Meta:
        model = products.Product
        fields = (
            'id',
            'name',
            'price',
            'remain',
            'main_image',
            'image_path',
            'images',
            'brand',
            'slug',
            'size',
            'size_type',
            'description',
            'discount',
            'type',
        )

    def get_image_path(self, obj):
        if obj.main_image:
            return obj.main_image.url


class ProductListSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    brand = BrandSerializer()

    class Meta:
        model = products.Product
        fields = (
            'id',
            'name',
            'price',
            'remain',
            'image_path',
            'slug',
            'brand',
            'views',
            'created_at',
            'discount'
        )

    def get_image_path(self, obj):
        if obj.main_image:
            return obj.main_image.url


class ProductPricesSerializer(serializers.Serializer):
    product_max_price = serializers.SerializerMethodField()
    product_min_price = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'product_max_price',
            'product_min_price'
        )

    def get_product_max_price(self, obj):
        return products.Product.objects.filter(active=1).aggregate(max_value=Max('price'))['max_value']

    def get_product_min_price(self, obj):
        return products.Product.objects.filter(active=1).aggregate(min_value=Min('price'))['min_value']