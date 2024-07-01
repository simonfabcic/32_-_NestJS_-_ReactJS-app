from rest_framework.permissions import SAFE_METHODS, BasePermission


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


class CanModifyOrViewOrder(BasePermission):
    """
    If HTTP method is 'GET', 'HEAD' or 'OPTIONS' (SAFE_METHODS), allow
    access if user has 'view_order' or 'change_order' permission,
    otherwise allow access only if user has 'change_order' permission.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user.has_perm("shop.view_order")
            or request.user.has_perm("shop.change_order")
        )
