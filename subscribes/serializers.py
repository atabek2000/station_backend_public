from rest_framework import serializers

from subscribes.models import Subscribe


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('email',) 