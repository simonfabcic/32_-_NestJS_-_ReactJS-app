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

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_items")

        # Create a list of item IDs that are present in the update data
        order_item_ids = [item["product"].id for item in order_items_data]

        # Delete any OrderItems that are no longer in the update data
        for order_item in instance.order_items.all():
            if order_item.product.id not in order_item_ids:
                order_item.delete()

        # Update or create OrderItems
        for order_item_data in order_items_data:
            try:
                order_item = OrderItem.objects.get(
                    order=instance,
                    product=order_item_data["product"],
                )
                order_item.quantity = order_item_data["quantity"]
                order_item.save()
            except OrderItem.DoesNotExist:
                OrderItem.objects.create(order=instance, **order_item_data)

        return instance
