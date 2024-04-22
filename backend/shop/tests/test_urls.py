from django.test import TestCase
from django.urls import reverse, resolve

from shop.views import getProfiles, profileNew, profile

class TestUrls(TestCase):
  
  def test_getProfiles_success_url_is_resolves(self):
    url = reverse("getProfiles")
    self.assertEquals(resolve(url).func, getProfiles)

  def test_profileNew_success_url_is_resolves(self):
    url = reverse("profileNew")
    self.assertEquals(resolve(url).func, profileNew)

  def test_profile_success_url_is_resolves(self):
    profile_id = 2
    url = reverse("profile", kwargs={'profile_id': profile_id})
    self.assertEquals(resolve(url).func, profile)