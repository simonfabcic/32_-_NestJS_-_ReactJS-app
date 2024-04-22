from django.urls import path
from . import views


urlpatterns = [
  path('profiles/', views.getProfiles, name="getProfiles"),
  path('profile/new', views.profileNew, name="profileNew"),
  path('profile/<str:profile_id>/', views.profile, name="profile"),
]