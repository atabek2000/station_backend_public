from rest_framework import serializers
from shop.models import brands, product_types


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = product_types.ProductType
        fields = (
            'id',
            'name',
        )
