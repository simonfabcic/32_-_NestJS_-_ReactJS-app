from django.contrib import admin

# from django.contrib.auth.models import User
from .models import CoreUser

# Register your models here.


# # Define an inline admin descriptor for Customer model
# # which acts a bit like a singleton
# class CustomerInline(admin.StackedInline):
#     model = Customer
#     can_delete = False
#     verbose_name_plural = "customer"


# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = [CustomerInline]


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

admin.site.register(CoreUser)
