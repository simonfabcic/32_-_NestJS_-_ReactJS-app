from django.urls import path

from . import views

urlpatterns = [
    # prefix "shop-api-v1/"
    path("profiles/", views.get_profiles, name="get_profiles"),
    path("profile/new", views.profile_create, name="profile_create"),
    path("profile/<str:profile_id>/", views.profile, name="profile"),
    path("role/", views.role_get, name="role_get"),
    path("permission/", views.permission_get, name="permission_get"),
    path("role/new/", views.role_create, name="role_create"),
    path("permission-user/", views.permission_user_get, name="permission_user"),
]
