from django.urls import path, include
from subscribes.views import SubscribeViewSet


urlpatterns = [
    path('subscribes/create/', SubscribeViewSet.as_view()),
]