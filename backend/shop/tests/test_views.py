from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import Permission, Group
from django.urls import reverse
import json

from shop.models import ShopProfile
from core.factory import CoreUserFactory
from shop.factory import ShopProfileFactory


class TestShopProfile(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "existing@example.com",
            "password": "secure_password",
            "avatar": "/dummy_image.com/259x267",
        }

    def test_shop_profile_add_success_adding_new_profile(self):
        no_of_shop_profiles_before = ShopProfile.objects.all().count()
        response = self.client.post(reverse("profile_create"), data=self.user_data)
        self.assertEqual(response.status_code, 201)
        no_of_shop_profiles_after = ShopProfile.objects.all().count()
        self.assertEqual(no_of_shop_profiles_before + 1, no_of_shop_profiles_after)

    def test_shop_profile_add_failure_adding_new_profile_duplicated_email(self):
        CoreUserFactory(email=self.user_data["email"])
        response = self.client.post(reverse("profile_create"), data=self.user_data)
        self.assertEqual(response.status_code, 409)
        # self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_shop_profile_add_failure_adding_new_profile_no_data(self):
        response = self.client.post(reverse("profile_create"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_shop_profile_add_failure_adding_new_profile_no_lastName(self):
        data_without_lastName = self.user_data.copy()
        del data_without_lastName["lastName"]
        response = self.client.post(
            reverse("profile_create"), data=data_without_lastName
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(ShopProfile.objects.all().count(), 0)

    def test_shop_profile_get_success(self):
        shop_profile = ShopProfileFactory()
        self.client.force_authenticate(user=shop_profile.user)

        self.assertEqual(ShopProfile.objects.all().count(), 1)

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        email_response = response.json()["email"]
        email_db = ShopProfile.objects.get(pk=shop_profile.id).user.email
        self.assertEqual(email_response, email_db)

    def test_shop_profile_get_failure_access_denied_unauthenticated(self):
        url = reverse("profile", kwargs={"profile_id": 2})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_shop_profile_update_success_update_all_fields(self):
        shop_profile = ShopProfileFactory()
        shop_profile_id = shop_profile.id
        self.client.force_authenticate(user=shop_profile.user)
        url = reverse("profile", kwargs={"profile_id": shop_profile_id})
        data_update = {
            "firstName": "Alice",
            "lastName": "Smith",
            "email": "alice@example.com",
            "password": "password",
            "userID": shop_profile_id,
        }
        data = json.dumps(data_update)
        response = self.client.put(
            url,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

        profile_after = ShopProfile.objects.get(id=shop_profile_id)
        self.assertEqual(shop_profile.user, profile_after.user)
        self.assertEqual(profile_after.user.email, data_update["email"])
        self.assertEqual(profile_after.first_name, data_update["firstName"])
        self.assertEqual(profile_after.last_name, data_update["lastName"])
        self.assertNotEqual(shop_profile.user.password, profile_after.user.password)

    def test_shop_profile_update_success_update_only_first_name(self):
        shop_profile = ShopProfileFactory()
        self.client.force_authenticate(user=shop_profile.user)
        shop_profile_id = shop_profile.id
        url = reverse("profile", kwargs={"profile_id": shop_profile_id})
        data_update = {
            "firstName": "John-changed",
            "userID": shop_profile_id,
        }
        data = json.dumps(data_update)
        response = self.client.put(
            url,
            data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

        profile_after = ShopProfile.objects.get(id=shop_profile_id)
        self.assertEqual(shop_profile.user, profile_after.user)
        self.assertEqual(shop_profile.user.email, profile_after.user.email)
        self.assertEqual(profile_after.first_name, data_update["firstName"])
        self.assertEqual(shop_profile.last_name, profile_after.last_name)
        self.assertEqual(shop_profile.user.password, profile_after.user.password)

    def test_shop_profile_create_success_create_if_not_exists(self):
        user = CoreUserFactory()
        self.client.force_authenticate(user=user)
        no_of_profiles = ShopProfile.objects.all().count()

        url = reverse("profile", kwargs={"profile_id": "null"})
        data_update = {
            "firstName": "Alice",
            "lastName": "Smith",
            "email": user.email,
            "userID": "null",
        }
        data = json.dumps(data_update)
        response = self.client.put(
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

    def test_shop_profile_update_failure_unauthenticated(self):
        url = reverse("profile", kwargs={"profile_id": 1})
        response = self.client.put(
            url,
        )
        self.assertEqual(response.status_code, 302)


class TestAvatar(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_avatar_get_success_get_img_url_from_shop_profile(self):
        shop_profile = ShopProfileFactory()

        self.client.force_authenticate(user=shop_profile.user)

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        avatar_response = response.json()["avatar"]
        avatar_db = ShopProfile.objects.get(pk=shop_profile.id).avatar
        self.assertEqual(avatar_response, avatar_db.url)

    def test_avatar_get_success_get_img_url_from_shop_profile_no_avatar(self):
        shop_profile = ShopProfileFactory(avatar=None)

        self.client.force_authenticate(user=shop_profile.user)

        url = reverse("profile", kwargs={"profile_id": shop_profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        avatar_response = response.json()["avatar"]
        self.assertEqual(avatar_response, None)

    def test_avatar_set_success_create_profile_containing_avatar_success(self):
        user_data = {
            "firstName": "Jane",
            "lastName": "Doe",
            "email": "existing@example.com",
            "password": "secure_password",
            "avatar": "/dummy_image.com/259x267",
        }

        response = self.client.post(reverse("profile_create"), data=user_data)
        self.assertEqual(response.status_code, 201)

        profile = ShopProfile.objects.get(user__email=user_data["email"])
        self.assertEqual(profile.avatar, user_data["avatar"])


class TestPermission(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CoreUserFactory()

    def test_permissions_get_success(self):
        permission_view_role = Permission.objects.get(codename="change_role")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        returned_codenames = {permission["codename"] for permission in response.data}
        expected_codenames = {
            "change_role",
            "view_role",
            "change_shopprofile",
            "view_shopprofile",
        }
        self.assertTrue(expected_codenames.issubset(returned_codenames))

    def test_permission_get_failure_authenticated_no_permission(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_permission_get_failure_not_authenticated(self):
        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_permission_get_failure_authenticated_wrong_permission(self):
        permission_view_role = Permission.objects.get(codename="view_shopprofile")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        url = reverse("permission_get")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class TestGroup(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CoreUserFactory()

        self.permission_change_role = Permission.objects.get(codename="change_role")

    # GET role
    def test_role_get_success(self):
        url = reverse("role_get")

        permission_view_role = Permission.objects.get(codename="view_role")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_role_get_failure_not_authenticated(self):
        url = reverse("role_get")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_role_get_failure_authenticated_no_permission(self):
        url = reverse("role_get")

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_role_get_failure_authenticated_wrong_permission(self):
        url = reverse("role_get")

        permission_change_role = Permission.objects.get(codename="change_role")
        self.user.user_permissions.add(permission_change_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # GET permission
    def test_permissions_get_success_permission_in_group(self):
        """
        The permission is not assigned to the user, but to the group in which the user is.
        """
        url = reverse("permission_get")

        group = Group.objects.create(name="test_group")
        permission_change_role = Permission.objects.get(codename="change_role")
        group.permissions.add(permission_change_role)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # PUT role
    def test_role_put_success(self):
        url = reverse("role_create")

        permission_change_role = Permission.objects.get(codename="change_role")
        self.user.user_permissions.add(permission_change_role)
        self.client.force_authenticate(user=self.user)

        no_of_groups_before = Group.objects.all().count()

        data = {"name": "role_name"}
        response = self.client.put(
            url,
            data,
        )
        self.assertEqual(response.status_code, 201)

        no_of_groups_after = Group.objects.all().count()
        self.assertEqual(no_of_groups_before + 1, no_of_groups_after)

    def test_role_put_failure_not_authenticated(self):
        url = reverse("role_create")

        no_of_groups_before = Group.objects.all().count()

        data = {"name": "role_name"}
        response = self.client.put(
            url,
            data,
        )
        self.assertEqual(response.status_code, 302)

        no_of_groups_after = Group.objects.all().count()
        self.assertEqual(no_of_groups_before, no_of_groups_after)

    def test_role_put_failure_authenticated_no_permission(self):
        url = reverse("role_create")

        self.client.force_authenticate(user=self.user)

        no_of_groups_before = Group.objects.all().count()

        data = {"name": "role_name"}
        response = self.client.put(
            url,
            data,
        )
        self.assertEqual(response.status_code, 403)

        no_of_groups_after = Group.objects.all().count()
        self.assertEqual(no_of_groups_before, no_of_groups_after)


class TestRoleAccessWithDifferentPermissions(APITestCase):
    def setUp(self):
        self.user = CoreUserFactory()
        self.url = reverse("role_get")

    def test_view_permissions_success_access_with_change_permission(self):
        permission_change_role = Permission.objects.get(codename="change_group")
        self.user.user_permissions.add(permission_change_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_permissions_success_access_with_view_permission(self):
        permission_view_role = Permission.objects.get(codename="view_group")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_permissions_success_superuser(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_permissions_failure_no_access_with_wrong_permission(self):
        permission_view_role = Permission.objects.get(codename="change_shopprofile")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
