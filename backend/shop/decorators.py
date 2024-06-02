from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission
from core.models import CoreUser


def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                raise PermissionDenied

            # Check if the user has the specific permission
            user = request.user
            app_label = "shop"
            if user.has_perm(f"{app_label}.{permission}"):
                return view_func(request, *args, **kwargs)

            # If the user does not have the permission, raise PermissionDenied
            raise PermissionDenied

        return _wrapped_view

    return decorator
