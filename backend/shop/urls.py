from django.urls import path
from rest_framework.routers import DefaultRouter
from shop import views

router = DefaultRouter()
router.register(r"order", views.OrderViewSet, basename="order")
router.register(r"order-item", views.OrderItemViewSet, basename="order-item")

urlpatterns = [
    # prefix "shop-api-v1/"
    path("profiles/", views.get_profiles, name="get_profiles"),
    path("profile/new", views.profile_create, name="profile_create"),
    path("profile/<str:profile_id>/", views.profile, name="profile"),
    path("role/", views.role_get, name="role_get"),
    path("role/new/", views.role_create, name="role_create"),
    path("permission/", views.permission_get, name="permission_get"),
    path("permission-user/", views.permission_user_get, name="permission_user"),
    path("product/", views.product_get, name="product_list"),
    path("product/<int:product_id>/", views.product_get, name="product_get"),
    path("product/create/", views.product_create, name="product_create"),
]

urlpatterns += router.urls
