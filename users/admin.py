from django.contrib import admin
from users.models.users import User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _
# from users.models.profile import Profile


# class ProfileAdmin(admin.StackedInline):
#     model = Profile
#     fields = ('telegram_id',)

@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'username', 'customer_type')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2'),
        }),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
    )
    list_display = ('id', 'full_name', 'email', 'phone_number',)

    list_display_links = ('id', 'full_name',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'customer_type')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    # inlines = (ProfileAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)