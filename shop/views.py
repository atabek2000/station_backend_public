from django.db import transaction, models
from django.db.models.functions import RowNumber, Coalesce
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProductFilter, BrandFilter, BrandSizeTypeFilter
from .models import products, product_types, brands, sizes
from shop.serializers.api.product import ProductSerializer, ProductListSerializer, ProductPricesSerializer
from django.http import Http404
from rest_framework import generics, filters, parsers, viewsets, mixins

from .models.brand_size_type import BrandSizeType
from .models.brands import Brand
from .models.news import News
from .models.product_types import ProductType
from .models.products import Product
from .models.size_types import SizeType
from .models.sizes import Size
from .serializers.api.brand import BrandSerializer, BrandMainSerializer
from .serializers.api.brand_size_type import BrandSizeTypeSerializer
from .serializers.api.news import NewsSerializer
from .serializers.api.product_type import ProductTypeSerializer
from .serializers.api.size import SizeSerializer
from django.db.models import Subquery, OuterRef, Count, Window, F, Prefetch

from .serializers.api.size_type import SizeTypeSerializer


# list of products
class ProductListViewSet(generics.ListAPIView):
    queryset = products.Product.objects.filter(active='1')
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'brand__name']


# one product by id
class ProductRetrieveViewSet(generics.RetrieveAPIView):
    queryset = products.Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductRetrieveSlugViewSet(generics.RetrieveAPIView):
    queryset = products.Product.objects.filter(active='1')
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = products.Product.objects.get(slug=kwargs['slug'])
            queryset.views += 1
            queryset.save()
        except Exception as error:
            print(error)
            raise Http404

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


# product types
class ProductTypeListViewSet(generics.ListAPIView):
    queryset = product_types.ProductType.objects.all()
    serializer_class = ProductTypeSerializer


# brands
class BrandListViewSet(generics.ListAPIView):
    queryset = brands.Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BrandFilter


# sizes
class SizeListViewSet(generics.ListAPIView):
    queryset = sizes.Size.objects.all()
    serializer_class = SizeSerializer


class SizeTypeListViewSet(generics.ListAPIView):
    queryset = SizeType.objects.all()
    serializer_class = SizeTypeSerializer


class BrandSizeTypeListViewSet(generics.ListAPIView):
    queryset = BrandSizeType.objects.all()
    serializer_class = BrandSizeTypeSerializer
    filterset_class = BrandSizeTypeFilter


class NewsListViewSet(generics.ListAPIView):
    queryset = News.objects.filter(active='1')
    serializer_class = NewsSerializer


class ImportProductData(APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES["excel"]
        success = ''
        error = ''
        counter = 0

        try:
            import openpyxl

            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active
            current_product = ''
            for row in worksheet.iter_rows(min_row=2, values_only=True):
                if row[1] is None:
                    continue
                counter += 1
                try:
                    with transaction.atomic():
                        current_product = row[0]

                        brand, brand_created = Brand.objects.get_or_create(name=row[6].strip())

                        prod_type, type_created = ProductType.objects.get_or_create(name=row[7].strip())

                        product, created = Product.objects.update_or_create(
                            name=row[0],
                            defaults={
                                'price': row[1],
                                'discount': row[2] if row[2] else 0,
                                'gender': 'm' if str(row[3]).strip() == 'm' else 'f',
                                'description': row[4],
                                'remain': row[5],
                                'brand': brand,
                                'type': prod_type
                            }
                        )

                        if created:
                            product.active = '0'

                        if row[8]:
                            sizes = str(row[8]).split(',')
                            for size in sizes:
                                sizeobj, spec_created = Size.objects.get_or_create(size=size)
                                product.size.add(sizeobj)
                        product.save()
                    success += f'{counter}) '+current_product+' ==> Создан!\n'
                except Exception as e:
                    print(e)
                    error += f'{counter}) '+current_product+' ==> '+str(e)+'\n'

            return render(request, 'admin/shop/product/upload.html', {'success': success, 'error': error})
        except Exception as e:
            return render(request, 'admin/shop/product/upload.html', {'success': success, 'error': error+str(e)})


class MainProductsView(generics.ListAPIView):
    serializer_class = BrandMainSerializer

    def get_queryset(self):
        prefetch_products = Prefetch(
            'products',
            queryset=Product.objects.filter(id__in=Subquery(Product.objects.filter(active=1).
                                                                      values_list('id', flat=True)))
        )

        queryset = Brand.objects.filter(show_on_main="1").order_by("-show_on_main_order").prefetch_related(prefetch_products)

        return queryset


class ProductPrices(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()[:1]
    serializer_class = ProductPricesSerializer
