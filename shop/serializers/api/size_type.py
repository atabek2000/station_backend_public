from rest_framework import serializers
from shop.models.size_types import SizeType
from shop.serializers.api.size import SizeSerializer


class SizeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeType
        fields = '__all__'
