from rest_framework.permissions import BasePermission


def can_view_groups(user):
    return (
        user.is_superuser
        or user.has_perm("auth.change_group")
        or user.has_perm("auth.view_group")
    )


def can_view_products(user):
    return (
        user.is_superuser
        or user.has_perm("shop.change_product")
        or user.has_perm("shop.view_product")
    )


class CanViewOrder(BasePermission):
    """
    Allows access only to logged in users with at least one of the permissions:
    shop.view_order or shop.change_order
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.has_perm("shop.view_order")
            or request.user.has_perm("shop.change_order")
        )


class CanModifyOrder(BasePermission):
    """
    Allows access only to logged in users with the shop.change_order permission
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            "shop.change_order"
        )
