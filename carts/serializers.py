from rest_framework import serializers
from store.models import Product
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_user']
        depth = 2


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'quantity', 'variations']
        depth = 1




