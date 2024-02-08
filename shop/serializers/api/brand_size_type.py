from rest_framework import serializers

from shop.models.brand_size_type import BrandSizeType
from shop.serializers.api.size_type import SizeTypeSerializer


class BrandSizeTypeSerializer(serializers.ModelSerializer):
    size_type = SizeTypeSerializer(read_only=True)
    class Meta:
        model = BrandSizeType
        fields = (
            'size_type',
            'product_type',
            'brand',
            'main',
                  )
