from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from core.models import User, Basket, Category, Product, Order, BasketProduct


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'address')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'amount', 'first_category')
    search_fields = ('name',)

    def first_category(self, obj):
        return obj.categories.first().name
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user',)
class BasketProductAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'amount')
    search_fields = ('basket',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'order_time', 'delivery_time')
    search_fields = ('user',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketProduct, BasketProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)