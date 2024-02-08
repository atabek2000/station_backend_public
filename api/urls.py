from api.spectacular.urls import urlpatterns as doc_urls
from django.urls import path, include
from users.urls import urlpatterns as user_urls
from shop.urls import urlpatterns as shop_urls
from order.urls import urlpatterns as order_urls
from subscribes.urls import urlpatterns as subscribe_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += doc_urls
urlpatterns += shop_urls
urlpatterns += user_urls
urlpatterns += order_urls
urlpatterns += subscribe_urls
