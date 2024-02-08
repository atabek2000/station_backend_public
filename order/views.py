from django.db import transaction
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from common.FFPay.getPayLink import getPayLink
from order.models import OrderItem, Order
from order.serializers import OrderSerializer, PaymentSerializer
from shop.models.products import Product


# Create your views here.

class OrderCreateView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            url = getPayLink(instance)
            return Response({"url": url},status=200)
        return Response('error',status=400)


class PaymentResultView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        # print(serializer.is_valid())
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            order = Order.objects.get(order_number=instance.pg_order_id)
            if (instance.pg_result == 1 or instance.pg_result == '1'):
                order.status = 'paid'
                order.payment = instance
            else:
                order.status = 'error'
                order.payment = instance
            order.save()
            return Response(status=200)
        return Response(status=400)



