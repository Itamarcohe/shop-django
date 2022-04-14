from django.contrib import admin

from store.models import Product
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'id', 'date_added')
    list_filter = ('cart_user', )


class CartItemAdmin(admin.ModelAdmin):
    list_filter = ('cart', 'product')
    list_display = ('cart', 'product', 'quantity', 'is_active', 'id')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)