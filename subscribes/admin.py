from django.contrib import admin

from subscribes.models import Subscribe


# Register your models here.
@admin.register(Subscribe)
class SubscribeRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at')
    list_display_links = ('id', 'email')
    readonly_fields = (
        'created_at', 'updated_at'
    )