from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import Permission
from django.urls import reverse


from core.factory import CoreUserFactory


class TestPermission(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CoreUserFactory()

    def test_get_permissions_success(self):
        permission_view_role = Permission.objects.get(codename="change_role")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_permission_failure_authenticated_no_permission(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_permission_failure_not_authenticated(self):
        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
