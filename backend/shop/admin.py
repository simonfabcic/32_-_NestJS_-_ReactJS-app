from django.contrib import admin
from django.contrib.auth.models import Permission

from shop.models import ShopProfile, Product

admin.site.register(ShopProfile)
admin.site.register(Permission)
admin.site.register(Product)
