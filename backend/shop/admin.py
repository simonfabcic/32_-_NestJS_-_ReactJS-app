from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission

admin.site.register(Role)
admin.site.register(ShopProfile)
admin.site.register(Permission)
