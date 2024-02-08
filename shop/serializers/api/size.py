from rest_framework import serializers
from shop.models import brands, sizes


class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = sizes.Size
        fields = (
            'id',
            'size',
        )
