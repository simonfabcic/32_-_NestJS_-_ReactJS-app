import json
from io import BytesIO

from core.factory import CoreUserFactory
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient, APITestCase
from shop.factory import ProductFactory, ShopProfileFactory
from shop.models import Product, ShopProfile


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
        self.url = reverse("permission_get")

    def test_permission_get_success_right_permissions_returned(self):
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        returned_codenames = {permission["codename"] for permission in response.data}
        expected_codenames = {
            "change_group",
            "view_group",
            "change_shopprofile",
            "view_shopprofile",
        }
        self.assertTrue(expected_codenames.issubset(returned_codenames))

    def test_permissions_get_success_permission_change_group(self):
        permission_view_role = Permission.objects.get(codename="change_group")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_permissions_get_success_permission_view_group(self):
        permission_view_role = Permission.objects.get(codename="view_group")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_permission_get_failure_authenticated_no_permission(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_permission_get_failure_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_permission_get_failure_authenticated_wrong_permission(self):
        permission_view_role = Permission.objects.get(codename="view_shopprofile")
        self.user.user_permissions.add(permission_view_role)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class TestGroup(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CoreUserFactory()

        self.permission_change_role = Permission.objects.get(codename="change_group")

    # GET role
    def test_role_get_success(self):
        url = reverse("role_get")

        permission_view_role = Permission.objects.get(codename="view_group")
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

        permission_change_role = Permission.objects.get(codename="change_shopprofile")
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
        permission_change_role = Permission.objects.get(codename="change_group")
        group.permissions.add(permission_change_role)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # PUT role
    def test_role_put_success(self):
        url = reverse("role_create")

        permission_change_group = Permission.objects.get(codename="change_group")
        self.user.user_permissions.add(permission_change_group)
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

    def test_role_put_failure_wrong_permission(self):
        url = reverse("role_create")

        permission_change_group = Permission.objects.get(codename="view_group")
        self.user.user_permissions.add(permission_change_group)
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


class TestPermissionGetCurrentUser(APITestCase):
    def setUp(self):
        self.user = CoreUserFactory()
        self.url = reverse("permission_user")

    def test_permissions_current_user_get_success_direct_assign_permission(self):
        perm_view_group = Permission.objects.get(codename="view_group")
        perm_view_shopprofile = Permission.objects.get(codename="view_shopprofile")
        self.user.user_permissions.add(perm_view_group)
        self.user.user_permissions.add(perm_view_shopprofile)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        permissions_excepted = ["auth.view_group", "shop.view_shopprofile"]
        permissions_response = response.json()["permissions"]
        self.assertEqual(set(permissions_excepted), set(permissions_response))

    def test_permissions_current_user_get_success_permission_in_group_and_direct(self):
        group = Group.objects.create(name="test_group")
        perm_view_group = Permission.objects.get(codename="view_group")
        group.permissions.add(perm_view_group)
        self.user.groups.add(group)
        perm_view_shopprofile = Permission.objects.get(codename="view_shopprofile")
        self.user.user_permissions.add(perm_view_shopprofile)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        permissions_excepted = ["auth.view_group", "shop.view_shopprofile"]
        permissions_response = response.json()["permissions"]
        self.assertEqual(set(permissions_excepted), set(permissions_response))


class TestGetShopProfiles(APITestCase):
    def setUp(self):
        self.user = CoreUserFactory()
        self.url = reverse("get_profiles")

    def test_get_shop_profiles_failure_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_shop_profiles_success(self):
        self.client.force_authenticate(user=self.user)

        # adding shop profile and assigning groups to it
        shop_profile = ShopProfileFactory()
        group = Group.objects.create(name="test_group_1")
        shop_profile.user.groups.add(group)
        group = Group.objects.create(name="test_group_2")
        shop_profile.user.groups.add(group)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        returned_groups = response.data["rows"][0]["groups"]
        expected_groups = ["test_group_1", "test_group_2"]

        # Assert that the returned groups match the expected groups
        self.assertEqual(set(returned_groups), set(expected_groups))


class TestProductGet(APITestCase):
    def setUp(self):
        self.user = CoreUserFactory()

        self.user_product_viewer = CoreUserFactory()
        perm_view_product = Permission.objects.get(codename="view_product")
        self.user_product_viewer.user_permissions.add(perm_view_product)

        self.user_product_editor = CoreUserFactory()
        perm_change_product = Permission.objects.get(codename="change_product")
        self.user_product_editor.user_permissions.add(perm_change_product)

        self.url_all = reverse("product_get_many")

    def test_product_get_success(self):
        self.client.force_authenticate(user=self.user_product_viewer)

        product = ProductFactory()
        response = self.client.get(self.url_all)
        self.assertEqual(response.status_code, 200)

        # check if returned data is product
        expected_keys = {"id", "image", "title", "description", "price"}
        self.assertTrue(expected_keys.issubset(response.data[0].keys()))

    def test_product_get_success_permission_change_product(self):
        self.client.force_authenticate(user=self.user_product_editor)

        response = self.client.get(self.url_all)
        self.assertEqual(response.status_code, 200)

    def test_product_get_failure_not_authenticated(self):
        response = self.client.get(self.url_all)
        self.assertEqual(response.status_code, 302)

    def test_product_get_failure_no_permissions(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url_all)
        self.assertEqual(response.status_code, 403)

    def test_product_get_one_success_using_product_id(self):
        self.client.force_authenticate(user=self.user_product_viewer)

        product = ProductFactory(title="test_title")
        url = reverse("product_get", kwargs={"product_id": product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["title"], "test_title")


class TestProductCreate(APITestCase):
    def setUp(self):
        self.user = CoreUserFactory()

        self.user_product_viewer = CoreUserFactory()
        perm_view_product = Permission.objects.get(codename="view_product")
        self.user_product_viewer.user_permissions.add(perm_view_product)

        self.user_product_editor = CoreUserFactory()
        perm_change_product = Permission.objects.get(codename="change_product")
        self.user_product_editor.user_permissions.add(perm_change_product)

        self.url = reverse("product_create")

        # create an in-memory image
        binary_stream = BytesIO()
        Image.new("RGB", (100, 100)).save(binary_stream, format="JPEG")
        # sets the file pointer to the beginning of the BytesIO object
        binary_stream.seek(0)
        self.product_data = {
            "image": SimpleUploadedFile(
                "test_image.jpg", binary_stream.read(), content_type="image/jpeg"
            ),
            "title": "how",
            "description": "Group sing charge piece cut more indicate.",
            "price": "566.04",
        }

    def test_product_create_success(self):
        self.client.force_authenticate(user=self.user_product_editor)

        no_of_products_before = Product.objects.all().count()

        response = self.client.put(self.url, data=self.product_data, format="multipart")
        self.assertEqual(response.status_code, 201)

        no_of_products_after = Product.objects.all().count()
        self.assertEqual(no_of_products_before + 1, no_of_products_after)

    def test_product_create_failure_not_authenticated(self):
        no_of_products_before = Product.objects.all().count()

        response = self.client.put(self.url, data=self.product_data, format="multipart")
        self.assertEqual(response.status_code, 302)

        no_of_products_after = Product.objects.all().count()
        self.assertEqual(no_of_products_before, no_of_products_after)

    def test_product_create_failure_no_permission(self):
        self.client.force_authenticate(user=self.user)

        no_of_products_before = Product.objects.all().count()

        response = self.client.put(self.url, data=self.product_data, format="multipart")
        self.assertEqual(response.status_code, 403)

        no_of_products_after = Product.objects.all().count()
        self.assertEqual(no_of_products_before, no_of_products_after)

    def test_product_create_failure_wrong_permission(self):
        self.client.force_authenticate(user=self.user_product_viewer)

        no_of_products_before = Product.objects.all().count()

        response = self.client.put(self.url, data=self.product_data, format="multipart")
        self.assertEqual(response.status_code, 403)

        no_of_products_after = Product.objects.all().count()
        self.assertEqual(no_of_products_before, no_of_products_after)
