from rest_framework import serializers
from shop.models import brands, products


class BrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = brands.Brand
        fields = (
            'id',
            'name',
            'image',
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url


class ProductMainSerializer(serializers.ModelSerializer):
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

class BrandMainSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    products = ProductMainSerializer(many=True, read_only=True)

    class Meta:
        model = brands.Brand
        fields = (
            'id',
            'name',
            'image',
            'show_on_main',
            'products',
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url