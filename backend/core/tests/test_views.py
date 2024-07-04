from core.factory import CoreUserFactory
from django.test import TestCase
from django.urls import reverse


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

    def test_get_token_success(self):
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            data={
                "email": self.email,
                "password": self.password,
            },
        )
        self.assertEqual(login_response.status_code, 200)

        data = login_response.json()
        self.assertIn("access", data)
        self.assertIn("access", data)
