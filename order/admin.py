from django.contrib import admin

from order.models import Payment, Order, OrderItem

########
#Inlines
class OrderOrderItemInline(admin.TabularInline):
    model = OrderItem



########

class OrderPaymentInline(admin.TabularInline):
    model = Order
    readonly_fields = ('order_number','status')
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'pg_payment_id', 'pg_order_id', 'pg_amount', 'pg_result', 'pg_user_phone')
    list_display_links = ('id','pg_payment_id', 'pg_order_id')
    list_filter = ('pg_result',)
    search_fields = ('pg_order_id', 'pg_amount', 'pg_user_phone')
    readonly_fields = (
        'pg_amount',
        'created_time',
        'pg_order_id',
        'pg_payment_id',
        'pg_ps_amount',
        'pg_ps_full_amount',
        'pg_ps_currency',
        'pg_description',
        'pg_user_phone',
        'pg_user_contact_email',
        'pg_payment_method',
        'pg_card_brand',
        'pg_result',
    )
    inlines = [OrderPaymentInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'order_number', 'status', 'amount')
    list_display_links = ('id', 'payment', 'order_number', 'status')
    readonly_fields = ('order_number',)
    list_filter = ('status',)
    inlines = [OrderOrderItemInline]
    # readonly_fields = (
    #     'order_number',
    #     'status',
    #     'amount',
    #     'created_time',
    #     'comment',
    #     'city',
    #     'delivery',
    #     'street',
    #     'house',
    #     'office',
    #     'intercom',
    #     'entrance',
    #     'floor',
    #     'payment',
    # )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'product_amount', 'discount')
    list_display_links = ('id', 'product')
    readonly_fields = [
        'order',
        'product',
        'quantity',
        'price',
        'discount',
    ]

    def product_amount(self, obj):
        return obj.quantity*obj.price

    product_amount.short_description = 'Стоимость'


# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'user', 'rating')
#     list_display_links = ('id', 'product')