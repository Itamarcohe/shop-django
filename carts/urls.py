from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    # path('<int:product_id>/', views.add_cart, name='cart'),


    path('add_to_cart', views.AddToCartView.as_view()),
    # path('add_to_cart', views.add_cart),


    path('get_cart', views.get_cart_items),

    path('remove-cart-item/<int:id>/', views.delete_cart_item),
    path('increase-cart-item/<int:id>/', views.increase_cart_item),
    path('reduce-cart-item/<int:id>/', views.reduce_from_cart_quantity),

    path('delete-cart/', views.delete_cart),


    path('checkout/', views.checkout)



]



