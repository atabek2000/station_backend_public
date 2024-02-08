from rest_framework import serializers
from shop.models.news import News


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'text',
            'image',
            'text_bottom',
            'link',
        )

    def get_image(self, obj):
        if obj.image:
            return obj.image.url