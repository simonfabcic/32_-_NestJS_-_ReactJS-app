from django.urls import path
from . import views


urlpatterns = [
  path('profiles/', views.getProfiles),
  path('profile/<str:profile_id>/', views.profile),
  path('profile/', views.profile),
]