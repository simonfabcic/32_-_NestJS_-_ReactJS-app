from django.test import TestCase
from django.urls import reverse, resolve


from rest_framework_simplejwt.views import TokenRefreshView
from core.views import MyTokenObtainPairView

class TestUrls(TestCase):
  
  def test_getProfiles_success_url_is_resolves(self):
    url = reverse("token_obtain_pair")
    self.assertEquals(resolve(url).func.view_class, MyTokenObtainPairView)

  def test_profileNew_success_url_is_resolves(self):
    url = reverse("token_refresh")
    self.assertEquals(resolve(url).func.view_class, TokenRefreshView)