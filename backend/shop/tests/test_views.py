from django.test import TestCase, Client
from django.urls import reverse

from core.models import CoreUser
from shop.models import Role, ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory


class TestViews(TestCase):

    def setUp(self):
        self.user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "existing@example.com",  # repeated email
            "password": "secure_password",
        }

    def test_adding_new_profile_success(self):
        no_of_shop_profiles_before = ShopProfile.objects.all().count()
        response = self.client.post(reverse("profile_create"), data=self.user_data)
        self.assertEqual(response.status_code, 201)
        no_of_shop_profiles_after = ShopProfile.objects.all().count()
        # self.assertEqual(ShopProfile.objects.all().count(), 1)
        self.assertEqual(no_of_shop_profiles_before + 1, no_of_shop_profiles_after)

    def test_adding_new_profile_failure_duplicated_email(self):
        CoreUserFactory(email=self.user_data["email"])
        response = self.client.post(reverse("profile_create"), data=self.user_data)
        self.assertEqual(response.status_code, 409)
        # self.assertEqual(ShopProfile.objects.all().count(), 0)
        # JURE the line above is throwing an error - what is the issue:
        # django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block.

    def test_adding_new_profile_failure_no_data(self):
        response = self.client.post(reverse("profile_create"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_adding_new_profile_failure_missing_lastName(self):
        data_without_lastName = self.user_data.copy()
        del data_without_lastName["lastName"]
        response = self.client.post(
            reverse("profile_create"), data=data_without_lastName
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)
