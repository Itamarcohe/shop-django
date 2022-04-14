from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from category.models import Category
from store.models import Product, Variation
from . serializers import ProductSerializer, CategorySerializer, VariationSerializer


@api_view(['GET'])
def menu_links(request):
    links = Category.objects.all()
    serializer = CategorySerializer(links, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def routes(request):
    api_urls = {
        'List':   '/api/products',
        'Detail': '/api/product-detail/<int:pk>/',
        'Create': '/api/product-create/',
        'Update': '/api/product-update/<int:pk>/',
        'Delete': '/api/product-delete/<int:pk>/',
        'Store': 'api/store/',
        'Products by category': 'api/store/<slug:category_slug>',
    }
    return Response(api_urls)


@api_view(['GET', 'POST'])
def products_list(request):
    """
    Get Products list,
    Sort Available by adding:
        ?range_by=max - for price from highest or min for lowest
        ?category=category_name - for specific category
        ?order=asc category_name - for ascending category name
        ?order=desc category_name - for descending category name

        ?min_range= will filter min price by the number  u insert
        ?max_range= will filter max price by the number  u insert


    """

    all_products = Product.objects.all().filter(is_available=True)

    if 'min_range' in request.GET:
        all_products = all_products.filter(price__gte=request.GET['min_range'])
    if 'max_range' in request.GET:
        all_products = all_products.filter(price__lte=request.GET['max_range'])

    if 'range_by' in request.GET:
        if request.GET['range_by'] == 'max':
            all_products = all_products.order_by('-price')
        if request.GET['range_by'] == 'min':
            all_products = all_products.order_by('price')

    if 'category' in request.GET and request.GET['category']:
        all_products = all_products.filter(category__category_name=request.GET['category'])

    if 'order' in request.GET:
        if request.GET['order'] == 'asc':
            all_products = all_products.order_by('category__category_name')
        if request.GET['order'] == 'desc':
            all_products = all_products.order_by('-category__category_name')

    if request.method == 'GET':
        serializer = ProductSerializer(all_products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse('Try again something went wrong')


@api_view(['GET'])
def productDetail(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def variationDetail(request, pk):
    product = Product.objects.get(id=pk)
    variation = Variation.objects.filter(product=product)
    serializer = VariationSerializer(variation, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def productCreate(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def productUpdate(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE', 'GET'])
def productDelete(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    if request.method == 'DELETE':
        product = Product.objects.get(id=pk)
        product.delete()
        return Response('Deleted product successfully')

