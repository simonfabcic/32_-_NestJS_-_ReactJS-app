from django.urls import path
from . import views


urlpatterns = [
    path("profiles/", views.get_profiles, name="get_profiles"),
    path("profile/new", views.profile_new, name="profile_new"),
    path("profile/<str:profile_id>/", views.profile, name="profile"),
    path("roles/", views.get_roles, name="get_roles"),
]
