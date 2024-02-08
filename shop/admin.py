from django.contrib import admin
from admin_extra_buttons.api import ExtraButtonsMixin, button, link
from django.shortcuts import render

from shop.models.brand_size_type import BrandSizeType
from shop.models.brands import Brand
from shop.models.news import News
from shop.models.product_images import ProductImage
from shop.models.product_types import ProductType
from shop.models.products import Product
from django.urls import reverse
from django.utils.html import format_html

from shop.models.size_types import SizeType
from shop.models.sizes import Size


###################################
# INLINES
###################################
class ProductImageInline(admin.TabularInline):
    model = ProductImage

###################################
# MODELS
###################################
@admin.register(Product)
class ProductAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'remain', 'brand', 'active', 'size_type')
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'brand__name',)
    list_editable = ('active','size_type')
    list_filter = ('active',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at', 'views'
    )

    inlines = [ProductImageInline]

    @button(
        label='Загрузить товары',
        html_attrs={
            'style': 'background-color: #3498db; color:white; padding: 10px; border-radius: 5px; cursor: pointer; user-select: none; text-decoration: none; margin-top:10px'})
    def refresh_1C(self, request):
        return render(request, 'admin/shop/product/upload.html')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )

@admin.register(ProductType)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')
    list_display_links = ('id', 'size',)
    search_fields = ('size',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )


@admin.register(SizeType)
class SizeTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_second', )
    list_display_links = ('id', 'name_second',)
    search_fields = ('name',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )


@admin.register(BrandSizeType)
class BrandSizeTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'product_type', 'size_type')
    list_display_links = ('id',)
    search_fields = ('brand',)
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'active', 'text_bottom')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'text')
    list_editable = ('image', 'active')
    readonly_fields = (
        'created_by', 'updated_by', 'created_at', 'updated_at'
    )

