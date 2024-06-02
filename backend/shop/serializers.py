from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    SerializerMethodField,
)
from shop.models import ShopProfile, Role
from django.contrib.auth.models import Permission, Group


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]


class ShopProfileSerializer(ModelSerializer):
    email = EmailField(source="user.email")
    full_name = SerializerMethodField()
    # role = CharField(source='role.name') # error if attribute not present
    role = SerializerMethodField()
    username = CharField(source="user.username")

    class Meta:
        model = ShopProfile
        fields = [
            "id",
            "email",
            "full_name",
            "first_name",
            "last_name",
            "role",
            "username",
            "avatar",
            # 'actions',
        ]

    def get_role(self, obj):
        return obj.role.name if obj.role else None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
