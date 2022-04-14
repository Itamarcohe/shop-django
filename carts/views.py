from rest_framework.generics import get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from . serializers import CartSerializer, CartItemSerializer
from rest_framework.views import APIView


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        product_variation = []
        product = get_object_or_404(Product, id=id)
        try:
            for item in request.GET:
                key = item
                value = request.GET[item]
                variation = Variation.objects.get(variation_category__iexact=key,
                                                       variation_value__iexact=value,
                                                       product=id)
                product_variation.append(variation)

        except Exception as e:
            print('reached exception')
            print(e)
        try:
            cart = Cart.objects.get(cart_user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_user=request.user
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        print('is cart item exist: ? ', is_cart_item_exists)
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variations_list = []
            cart_item_id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                existing_variations_list.append(list(existing_variation))
                cart_item_id.append(item.id)

            if product_variation in existing_variations_list or product_variation[::-1] in existing_variations_list:
                print('its in existing var list we got it!')
                try:
                    index = existing_variations_list.index(product_variation)
                except ValueError:
                    index = existing_variations_list.index(product_variation[::-1])

                item_id = cart_item_id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    cart = get_object_or_404(Cart, cart_user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def increase_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.quantity += 1
    cart_item.save()
    product = get_object_or_404(Product, id=cart_item.product.id)
    product.stock -= 1
    product.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reduce_from_cart_quantity(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    product = get_object_or_404(Product, id=cart_item.product.id)
    if cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()
        product.stock += 1
        product.save()

    if cart_item.quantity < 1:
        cart_item.delete()
    else:
        cart_item.save()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['DELETE', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    cart = get_object_or_404(Cart, cart_user=request.user)
    cart.delete()
    # print(id)
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE', 'GET'])
def delete_cart_item(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    total_items = cart_item.quantity
    product = get_object_or_404(Product, id=cart_item.product.id)
    product.stock += total_items
    product.save()
    cart_item.delete()
    print(id)
    return Response(status=status.HTTP_200_OK)


def cart(request):
    cart = 'cart'
    return Response(cart)


def checkout(request):
    return Response('Checkout')