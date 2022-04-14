from rest_framework.response import Response
from rest_framework.decorators import api_view
import uuid
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from accounts.models import Account
from carts.models import CartItem, Cart
from orders.models import Order
from orders.serializers import OrderSerializer


# @api_view(['GET', 'POST'])
# def place_order(request, total=0, quantity=0):
#     current_user = request.user.id
#     cart_user = Account.objects.get(id=current_user)
#     cart = Cart.objects.get(cart_user=cart_user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     for cart_item in cart_items:
#         total += (cart_item.quantity * cart_item.product.price)
#         quantity += cart_item.quantity
#     tax = (total * 0.03)
#     grand_total = total + tax
#     request.data["user_id"] = current_user
#     request.data["order_total"] = grand_total
#     request.data["tax"] = tax
#     request.data["ip"] = request.META.get('REMOTE_ADDR')
#     request.data["order_number"] = str(uuid.uuid1())
#     if request.method == 'POST':
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#
#     return Response(serializer.data)


@api_view(['GET'])
def payments(request):
    print('i have been called')
    try:
        order = Order.objects.get(user_id=request.user.id)
        serializer = OrderSerializer(order, many=False)
    except:
        return Response(False)
    return Response(serializer.data)


@api_view(['DELETE', 'GET'])
def delete_order(request):
    order = Order.objects.get(user_id=request.user.id)
    serializer = OrderSerializer(order, many=False)
    if request.method == 'GET':
        order = Order.objects.get(user_id=request.user.id)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':
        order = Order.objects.get(user_id=request.user.id)
        order.delete()
        return Response(serializer.data)



# @api_view(['GET', 'POST', 'PUT'])
# def place_order(request, total=0, quantity=0):
#     current_user = request.user.id
#     cart_user = Account.objects.get(id=current_user)
#     cart = Cart.objects.get(cart_user=cart_user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     for cart_item in cart_items:
#         total += (cart_item.quantity * cart_item.product.price)
#         quantity += cart_item.quantity
#         print('in cart loop')
#     tax = (total * 0.03)
#     grand_total = total + tax
#     request.data["user_id"] = current_user
#     request.data["order_total"] = grand_total
#     request.data["tax"] = tax
#     request.data["ip"] = request.META.get('REMOTE_ADDR')
#     request.data["order_number"] = str(uuid.uuid1())
#     try:
#         order = Order.objects.get(user_id=current_user)
#         serializer = OrderSerializer(order, data=request.data)
#         print('in put')
#         if serializer.is_valid():
#             print('in put valid')
#
#             serializer.save()
#             return Response(serializer.data)
#         print(serializer.errors)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#
#     except ObjectDoesNotExist:
#         serializer = OrderSerializer(data=request.data)
#         print('in POST')
#         if serializer.is_valid():
#             print('in validation')
#             serializer.save()
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         print(serializer.errors)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PUT'])
def place_order(request, total=0, quantity=0):
    current_user = request.user.id
    cart_user = Account.objects.get(id=current_user)
    cart = Cart.objects.get(cart_user=cart_user)
    cart_items = CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        total += (cart_item.quantity * cart_item.product.price)
        quantity += cart_item.quantity
        print('in cart loop')
    tax = (total * 0.03)
    grand_total = total + tax
    request.data["user_id"] = current_user
    request.data["order_total"] = grand_total
    request.data["tax"] = tax
    request.data["ip"] = request.META.get('REMOTE_ADDR')
    request.data["order_number"] = str(uuid.uuid1())
    print(grand_total)
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        print('in POST')

        if serializer.is_valid():
            print('in validation')

            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        order = Order.objects.get(user_id=current_user)
        if request.data['first_name'] == "":
            request.data['first_name'] = order.first_name
        if request.data['last_name'] == "":
            request.data['last_name'] = order.last_name
        if request.data['phone'] == "":
            request.data['phone'] = order.phone
        if request.data['email'] == "":
            request.data['email'] = order.email
        if request.data['address_line_1'] == "":
            request.data['address_line_1'] = order.address_line_1
        if request.data['city'] == "":
            request.data['city'] = order.city
        if request.data['country'] == "":
            request.data['country'] = order.country
        if request.data['order_note'] == "":
            request.data['order_note'] = order.order_note
        if request.data['address_line_2'] == "":
            request.data['address_line_2'] = order.address_line_2
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



