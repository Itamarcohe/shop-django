from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ProductAPIView

urlpatterns = [


    path('admin/', admin.site.urls),
    path('', views.routes),
    path('api/store/', include('store.urls')),
    path('api/cart/', include('carts.urls')),
    path('api/products', views.products_list),
    path('api/category_links', views.menu_links),
    path('api/product-detail/<int:pk>/', views.productDetail),
    path('api/variation-detail/<int:pk>/', views.variationDetail),
    path('api/product-create/', views.productCreate),
    path('api/product-update/<int:pk>/', views.productUpdate),
    path('api/product-delete/<int:pk>/', views.productDelete),
    path('api/store/', include('store.urls')),
    path('api/user/', include('accounts.urls', namespace='accounts')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/orders/', include('orders.urls')),


    path('api/search/', ProductAPIView.as_view()),

]
