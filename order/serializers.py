from django.db import transaction
from rest_framework import serializers

from order.models import Order, OrderItem, Payment
from shop.models.products import Product
from shop.serializers.api.product import ProductSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ('id',)

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderProductSerializer()

    class Meta:
        model = OrderItem

        fields = (
            'quantity',
            'product'
        )

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order

        fields = (
            "amount",
            "comment",
            "country",
            "city",
            "delivery",
            "street",
            "house",
            "office",
            "intercom",
            "entrance",
            "floor",
            "order_items",
        )

    def create(self, validated_data):
        try:
            with transaction.atomic():
                order_items = validated_data.pop('order_items')
                order = Order.objects.create(**validated_data)
                for order_item in order_items:
                    product = Product.objects.get(id=order_item['product']['id'])
                    order_item.pop('product')
                    OrderItem.objects.create(order=order, quantity=order_item['quantity'], price=product.price, product=product)

                return order
        except Exception as e:
            raise serializers.ValidationError(str(e))


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        exclude = ['created_time']