from django.contrib import admin
from .models import Order, Payment, OrderProduct

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)