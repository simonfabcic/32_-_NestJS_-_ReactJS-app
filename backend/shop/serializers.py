from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    SerializerMethodField,
)
from shop.models import Order, Product, ShopProfile


class ShopProfileSerializer(ModelSerializer):
    email = EmailField(source="user.email")
    full_name = SerializerMethodField(read_only=True)
    username = CharField(source="user.username")
    groups = SerializerMethodField(read_only=True)

    class Meta:
        model = ShopProfile
        fields = [
            "id",
            "email",
            "full_name",
            "first_name",
            "last_name",
            "username",
            "avatar",
            "groups",
            # 'actions',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_groups(self, obj):
        return [group.name for group in obj.user.groups.all()]


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "image", "title", "description", "price"]


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        # fields = ["order_item"]
