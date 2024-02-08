from django.shortcuts import render
from rest_framework import generics

from subscribes.models import Subscribe
from subscribes.serializers import SubscribeSerializer


# Create your views here.


class SubscribeViewSet(generics.CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer