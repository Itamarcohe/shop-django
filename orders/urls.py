from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order),
    path('payments/', views.payments),
    path('delete_order/', views.delete_order)

]
