from django.test import TestCase, Client
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import json

from shop.models import ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory


class TestViews(TestCase):

    def setUp(self):
        self.user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "existing@example.com",
            "password": "secure_password",
            "avatar": "/dummy_image.com/259x267",
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

    def test_get_profile_success(self):
        shop_profile = ShopProfileFactory()
        self.assertEqual(ShopProfile.objects.all().count(), 1)

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client_with_access_token.get(url)

        self.assertEqual(response.status_code, 200)

        email_response = response.json()["email"]
        email_db = ShopProfile.objects.get(pk=shop_profile.id).user.email
        self.assertEqual(email_response, email_db)

    def test_get_profile_failure_access_denied_unauthorized(self):
        url = reverse("profile", kwargs={"profile_id": 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_shop_profile_update_all_success(self):
        profile = ShopProfileFactory()
        profile_id = profile.id
        url = reverse("profile", kwargs={"profile_id": profile_id})
        data_update = {
            "firstName": "Alice",
            "lastName": "Smith",
            "email": "alice@example.com",
            "password": "password",
            "userID": profile_id,
        }
        data = json.dumps(data_update)
        response = self.client_with_access_token.put(
            url,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

        profile_after = ShopProfile.objects.get(id=profile_id)
        self.assertEqual(profile.user, profile_after.user)
        self.assertEqual(profile_after.user.email, data_update["email"])
        self.assertEqual(profile_after.first_name, data_update["firstName"])
        self.assertEqual(profile_after.last_name, data_update["lastName"])
        self.assertNotEqual(profile.user.password, profile_after.user.password)

    def test_shop_profile_update_only_first_name(self):
        profile = ShopProfileFactory()
        profile_id = profile.id
        url = reverse("profile", kwargs={"profile_id": profile_id})
        data_update = {
            "firstName": "John-changed",
            "userID": profile_id,
        }
        data = json.dumps(data_update)
        response = self.client_with_access_token.put(
            url,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

        profile_after = ShopProfile.objects.get(id=profile_id)
        self.assertEqual(profile.user, profile_after.user)
        self.assertEqual(profile.user.email, profile_after.user.email)
        self.assertEqual(profile_after.first_name, data_update["firstName"])
        self.assertEqual(profile.last_name, profile_after.last_name)
        self.assertEqual(profile.user.password, profile_after.user.password)

    def test_shop_profile_create_if_not_exists_success(self):
        user = CoreUserFactory()
        no_of_profiles = ShopProfile.objects.all().count()

        url = reverse("profile", kwargs={"profile_id": "null"})
        data_update = {
            "firstName": "Alice",
            "lastName": "Smith",
            "email": user.email,
            "userID": "null",
        }
        data = json.dumps(data_update)
        response = self.client_with_access_token.put(
            url,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        no_of_profiles_after = ShopProfile.objects.all().count()
        self.assertEqual(no_of_profiles + 1, no_of_profiles_after)

        profile = ShopProfile.objects.get(user__email=user.email)

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.user.email, data_update["email"])
        self.assertEqual(profile.first_name, data_update["firstName"])
        self.assertEqual(profile.last_name, data_update["lastName"])

    def test_shop_profile_update_failure_not_signed_in(self):
        url = reverse("profile", kwargs={"profile_id": 1})
        response = self.client.put(
            url,
        )
        self.assertEqual(response.status_code, 401)

    def test_shop_profile_get_img_url(self):
        shop_profile = ShopProfileFactory()

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client_with_access_token.get(url)
        self.assertEqual(response.status_code, 200)

        avatar_response = response.json()["avatar"]
        avatar_db = ShopProfile.objects.get(pk=shop_profile.id).avatar
        self.assertEqual(avatar_response, avatar_db.url)

    def test_shop_profile_no_img_url(self):
        shop_profile = ShopProfileFactory(avatar=None)

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client_with_access_token.get(url)
        self.assertEqual(response.status_code, 200)

        avatar_response = response.json()["avatar"]
        self.assertEqual(avatar_response, None)
