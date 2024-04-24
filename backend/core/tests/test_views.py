from django.test import TestCase, Client
from django.urls import reverse

from core.models import CoreUser
from shop.models import Role, ShopProfile

from shop.factory import ShopProfileFactory
from core.factory import CoreUserFactory


class TestAuthAPI(TestCase):
    def setUp(self):
        self.email = "existing@example.com"
        self.password = "secure_password"
        self.core_user = CoreUserFactory(email=self.email, password=self.password)

    def test_token_obtain_pair_success(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            data=data,
        )
        self.assertEqual(login_response.status_code, 200)

    def test_token_obtain_pair_failure_incorrect_password(self):
        data = {"email": self.email, "password": "wrong_password"}
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            data=data,
        )
        self.assertEqual(login_response.status_code, 401)
