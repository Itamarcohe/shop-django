from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from category.models import Category
from shopping.serializers import ProductSerializer
from store.models import Product


# Create your views here.

class StoreList(generics.ListAPIView):
    queryset = Product.objects.all().filter(is_available=True)
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name', 'price', 'id', 'category']


@api_view(['GET'])
def by_category(request, category_slug=None):

    # not really need thoose
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    products = Product.objects.all().filter(is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

