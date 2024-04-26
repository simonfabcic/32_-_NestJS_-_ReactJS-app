from django.test import TestCase, Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.models import CoreUser
from shop.models import Role, ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory


class TestViews(TestCase):

    def setUp(self):
        self.user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "existing@example.com",
            "password": "secure_password",
        }
        self.user = CoreUserFactory()

        self.client_with_access_token = Client()
        refresh_token = RefreshToken.for_user(self.user)
        headers = {"Authorization": f"Bearer {refresh_token.access_token}"}
        self.client_with_access_token.defaults["HTTP_AUTHORIZATION"] = headers[
            "Authorization"
        ]

    def test_adding_new_profile_success(self):
        no_of_shop_profiles_before = ShopProfile.objects.all().count()
        response = self.client.post(reverse("profile_new"), data=self.user_data)
        self.assertEqual(response.status_code, 201)
        no_of_shop_profiles_after = ShopProfile.objects.all().count()
        # self.assertEqual(ShopProfile.objects.all().count(), 1)
        self.assertEqual(no_of_shop_profiles_before + 1, no_of_shop_profiles_after)

    def test_adding_new_profile_failure_duplicated_email(self):
        CoreUserFactory(email=self.user_data["email"])
        response = self.client.post(reverse("profile_new"), data=self.user_data)
        self.assertEqual(response.status_code, 409)
        # self.assertEqual(ShopProfile.objects.all().count(), 0)
        # JURE the line above is throwing an error - what is the issue:
        # django.db.transaction.TransactionManagementError: An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block.

    def test_adding_new_profile_failure_no_data(self):
        response = self.client.post(reverse("profile_new"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_adding_new_profile_failure_missing_lastName(self):
        data_without_lastName = self.user_data.copy()
        del data_without_lastName["lastName"]
        response = self.client.post(reverse("profile_new"), data=data_without_lastName)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_get_profile_success(self):
        for _ in range(1, 4):
            ShopProfileFactory()
        self.assertEqual(ShopProfile.objects.all().count(), 3)

        for profile_id in range(1, 4):
            url = reverse("profile", kwargs={"profile_id": profile_id})
            response = self.client_with_access_token.get(url)

            self.assertEqual(response.status_code, 200)

            email_response = response.json()["email"]
            email_db = ShopProfile.objects.get(pk=profile_id).user.email
            self.assertEqual(email_response, email_db)

    def test_get_profile_failure_access_denied_unauthorized(self):
        url = reverse("profile", kwargs={"profile_id": 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    # TODO Implement tests for update user
