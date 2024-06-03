from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, Permission
from core.models import CoreUser
from django.http import HttpResponse


def permission_required(*permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return HttpResponse("Unauthorized", status=401)

            # Check if the user has the specific permission (or users group)
            user = request.user
            app_label = "shop"
            if any(user.has_perm(f"{app_label}.{perm}") for perm in permissions):
                return view_func(request, *args, **kwargs)

            # If the user does not have the permission, raise PermissionDenied
            raise PermissionDenied

        return _wrapped_view

    return decorator
