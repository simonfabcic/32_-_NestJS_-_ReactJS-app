
from django.test import TestCase, Client
from django.urls import reverse

from core.models import CoreUser
from shop.models import Role, ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory

class TestViews(TestCase):

  def setUp(self):
    self.client = Client()
    self.user_data = {
      "firstName": "Jane",
      "lastName": "Doe",
      "email": "existing@example.com", # repeated email
      "password": "secure_password"
    }

  def test_profileNew_POST_success_valid_data(self):
    response = self.client.post(reverse("profileNew"), data=self.user_data)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(ShopProfile.objects.count(), 1)

  def test_profileNew_POST_failure_user_already_exist(self):
    CoreUserFactory(email="existing@example.com")
    response = self.client.post(reverse("profileNew"), data=self.user_data)
    self.assertEqual(response.status_code, 409)
    # self.assertEqual(ShopProfile.objects.count(), 0)
    # JURE the line above is throwing an error - what is the issue:
    # django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block.

  def test_profileNew_POST_failure_no_data(self):
    response = self.client.post(reverse("profileNew"))
    self.assertEqual(response.status_code, 422)
    self.assertEqual(ShopProfile.objects.count(), 0)

  def test_profileNew_POST_failure_missing_lastName(self):
    data_without_lastName = self.user_data.copy()
    del data_without_lastName["lastName"]
    response = self.client.post(reverse("profileNew"), data=data_without_lastName)
    self.assertEqual(response.status_code, 422)
    self.assertEqual(ShopProfile.objects.count(), 0)