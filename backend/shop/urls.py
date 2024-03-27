from django.urls import path
from . import views


urlpatterns = [
  path('profiles/', views.getProfiles),
  path('profile/<str:username>/', views.profile)
]