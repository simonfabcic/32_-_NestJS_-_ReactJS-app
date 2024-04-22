
from django.test import TestCase, Client
from django.urls import reverse

from core.models import CoreUser
from shop.models import Role, ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory

class TestViews(TestCase):

  def setUp(self):
    self.client = Client()
    self.core_user_data = {
      "firstName": "Jane",
      "lastName": "Doe",
      "email": "existing@example.com", # repeated email
      "password": "secure_password"
    }
    self.core_user = CoreUserFactory(
      email = self.core_user_data["email"],
      password = self.core_user_data["password"]
    )


  def test_MyTokenObtainPairSerializer_POST_success_user_login(self):
    login_response = self.client.post(
      reverse('token_obtain_pair'),
      data = {"email": self.core_user_data["email"], "password": self.core_user_data["password"]},
      content_type='application/json'
    )
    self.assertEqual(login_response.status_code, 200)

  def test_MyTokenObtainPairSerializer_POST_failure_wrong_password(self):
    login_response = self.client.post(
      reverse('token_obtain_pair'),
      data = {"email": self.core_user_data["email"], "password": "wrong_password"},
      content_type='application/json'
    )
    self.assertEqual(login_response.status_code, 401)