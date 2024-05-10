from django.urls import path
from . import views


urlpatterns = [
    path("profiles/", views.getProfiles, name="get_profiles"),
    path("profile/new", views.profileNew, name="profile_new"),
    path("profile/<str:profile_id>/", views.profile, name="profile"),
    path("roles/", views.getRoles, name="get_roles"),
]
