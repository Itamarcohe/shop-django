from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreList.as_view(), name='store'),
    path('<slug:category_slug>/', views.by_category, name='product_by_category'),

]
