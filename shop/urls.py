from django.urls import path, include

from order.views import OrderCreateView
from .views import ProductListViewSet, ProductRetrieveViewSet, ProductTypeListViewSet, BrandListViewSet, \
    SizeListViewSet, ProductRetrieveSlugViewSet, NewsListViewSet, ImportProductData, MainProductsView, ProductPrices, \
    SizeTypeListViewSet, BrandSizeTypeListViewSet
from rest_framework import routers
# app name for namespace
app_name = 'product'

shop_router = routers.DefaultRouter()

shop_router.register(r'product_prices', ProductPrices, basename='product_prices')

urlpatterns = [
    path('', include(shop_router.urls)),  # products urls
    path('product/', ProductListViewSet.as_view(),),
    path('main_products/', MainProductsView.as_view(),),
    path('product/<int:id>', ProductRetrieveViewSet.as_view(),),
    path('product/<str:slug>', ProductRetrieveSlugViewSet.as_view()),
    path('product_type/', ProductTypeListViewSet.as_view(),),
    path('brand/', BrandListViewSet.as_view(),),
    path('product_size/', SizeListViewSet.as_view(),),
    path('product_size_type/', SizeTypeListViewSet.as_view(),),
    path('brand_size_type/', BrandSizeTypeListViewSet.as_view(),),
    path('news/', NewsListViewSet.as_view(),),
    path('import', ImportProductData.as_view()),
]
