from django.urls import path, include

from order.views import OrderCreateView, PaymentResultView

app_name = 'order'

urlpatterns = [
    path('order/create/', OrderCreateView.as_view() ,),
    path('pay/result/', PaymentResultView.as_view() ,),
]