from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    SerializerMethodField,
)
from shop.models import ShopProfile


class ShopProfileSerializer(ModelSerializer):
    email = EmailField(source="user.email")
    full_name = SerializerMethodField()
    # role = CharField(source='role.name') # error if attribute not present
    # role = SerializerMethodField()
    # group = SerializerMethodField()
    username = CharField(source="user.username")

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
            # 'actions',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
