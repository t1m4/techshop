from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from core.models import User, Basket


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, MyUserAdmin)
admin.site.register(Basket)