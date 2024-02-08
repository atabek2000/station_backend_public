import django_filters
from django.db.models import Q

from .models import sizes, products
from .models.brand_size_type import BrandSizeType
from .models.brands import Brand
from .models.products import Product
from .models.size_types import SizeType


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')
    # gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')
    gender = django_filters.CharFilter(field_name='gender', method='filter_gender')
    brand_id = NumberInFilter(field_name='brand__id')
    type_id = NumberInFilter(field_name='type__id')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    size = django_filters.ModelMultipleChoiceFilter(field_name='size__size', to_field_name='size', queryset=sizes.Size.objects.all())
    discount = django_filters.NumberFilter(field_name='discount', lookup_expr='gte')

    def filter_gender(self, queryset, name, value):
        values = value.split(',')  # Assuming values are comma-separated
        return queryset.filter(**{'{}__in'.format(name): values})

    class Meta:
        model = Product
        fields = ('name',)

class BrandFilter(django_filters.FilterSet):
    show_on_main = django_filters.CharFilter(field_name='show_on_main')

    class Meta:
        model = Brand
        fields = ('show_on_main',)


class BrandSizeTypeFilter(django_filters.FilterSet):
    brand = django_filters.NumberFilter(method='filter_brand_id')
    product_type = NumberInFilter(field_name='product_type__id')

    class Meta:
        model = BrandSizeType
        fields = ('brand', 'product_type',)

    def filter_brand_id(self, queryset, name, value):
        if value:
            return queryset.filter(Q(brand__id=value) | Q(brand__id__isnull=True))
        return queryset
