from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)
from shop.models import Order, OrderItem, Product, ShopProfile


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


class OrderItemSerializer(ModelSerializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all())
    order = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]


class OrderSerializer(ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "order_items"]

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order
