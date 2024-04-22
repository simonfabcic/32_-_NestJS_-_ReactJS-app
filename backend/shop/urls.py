from django.urls import path
from . import views


urlpatterns = [
  path('profiles/', views.getProfiles),
  path('profile/new', views.profileNew),
  path('profile/<str:profile_id>/', views.profile),
]