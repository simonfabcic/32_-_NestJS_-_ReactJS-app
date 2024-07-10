from django.contrib import admin
from django.contrib.auth.models import Permission

from shop.models import ShopProfile, Product, Order, OrderItem

admin.site.register(Permission)
admin.site.register(ShopProfile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
