from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import *

admin.site.register(ShopProfile)
admin.site.register(Permission)
admin.site.register(Product)
