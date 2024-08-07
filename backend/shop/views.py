from django.core.exceptions import ValidationError
from core.models import CoreUser
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shop.models import Order, Product, ShopProfile, OrderItem
from shop.permissions import CanModifyOrViewOrder, can_view_groups, can_view_products
from shop.serializers import (
    GroupSerializer,
    OrderSerializer,
    PermissionSerializer,
    ProductSerializer,
    ShopProfileSerializer,
    OrderItemSerializer,
)
from django.core.paginator import EmptyPage


@api_view(["GET"])
@login_required()
# URL: /profiles?page=[int]&page_size=[int]&sort_by=[options]&sort_order=[asc|desc]
def get_profiles(request):
    headers = [
        {"key": "avatar", "label": "Avatar", "sorting": False},
        {"key": "email", "label": "Email", "sorting": False},
        {"key": "full_name", "label": "Full name", "sorting": True},
        {"key": "group", "label": "Role", "sorting": False},
    ]

    # set default sorting field - first available from "headers"
    for header in headers:
        if header["sorting"]:
            default_sort_by = header["key"]
            break

    # setting variables from URL
    current_page = request.GET.get("page", "1")
    page_size = request.GET.get("page_size", "15")
    sort_by = request.GET.get("sort_by", default_sort_by)
    sort_order = request.GET.get("sort_order", "ASC")

    # checking if URL parameters are OK, if not return error '400'
    if not (
        current_page.isdigit()
        and page_size.isdigit()
        and any(header["key"] == sort_by for header in headers)
        and sort_order in ["ASC", "DESC"]
    ):
        # prepare data to return in case of error
        sortingOptions = ""
        for header in headers:
            if len(sortingOptions) > 0:
                sortingOptions += "|"
            sortingOptions = sortingOptions + header["key"]
        options = (
            "/profiles?page=[int]&page_size=[int]&sort_by=["
            + sortingOptions
            + "]&sort_order=[asc|desc]"
        )
        return Response(
            {"error": "Error in parameters.", "options": options},
            status=status.HTTP_400_BAD_REQUEST,
        )

    current_page = int(current_page)
    page_size = int(page_size)

    if sort_by == "full_name":
        profiles = ShopProfile.objects.all().order_by("first_name", "last_name")
    else:
        profiles = ShopProfile.objects.all().order_by(sort_by)

    if sort_order == "DESC":
        profiles = profiles.reverse()

    p = Paginator(profiles, page_size)
    try:
        page = p.page(current_page)
    except EmptyPage:
        return Response(
            {"error": "Parameters 'page' and 'page_size' not compatible"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = ShopProfileSerializer(page.object_list, many=True)
    serialized_rows = serializer.data

    pagination_description = {
        "sort_order": sort_order,
        "sort_by": sort_by,
        "total_records": p.count,
        "total_pages": p.num_pages,
        "current_page": current_page,
        "prev_page": page.previous_page_number() if page.has_previous() else None,
        "next_page": page.next_page_number() if page.has_next() else None,
        "page_size": page_size,
    }

    return Response(
        {
            "headers": headers,
            "rows": serialized_rows,
            "pagination_description": pagination_description,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def profile_create(request):
    firstName = request.data.get("firstName")
    lastName = request.data.get("lastName")
    email = request.data.get("email")
    password = request.data.get("password")
    avatar = request.data.get("avatar")
    if not (firstName and lastName and email and password):
        return Response(
            {"message": "Fail. Profile not created."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    try:
        user = CoreUser.objects.create_user(
            username=email, email=email, password=password
        )
        ShopProfile.objects.create(
            user=user,
            first_name=firstName,
            last_name=lastName,
            avatar=avatar,
        )
        return Response(
            {"message": "Success. Profile created."}, status=status.HTTP_201_CREATED
        )
    except IntegrityError:
        return Response(
            {"error": "Email already taken."}, status=status.HTTP_409_CONFLICT
        )
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response(
            {"error": "Error creating new user."}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["PUT", "GET", "DELETE"])
@login_required()
def profile(request, profile_id):
    match request.method:
        case "PUT":
            firstName = request.data.get("firstName")
            lastName = request.data.get("lastName")
            email = request.data.get("email")
            password = request.data.get("password")
            avatar = request.data.get("avatar")
            try:
                if profile_id == "null":
                    raise ObjectDoesNotExist("URL parameter profileID is 'null'.")
                profile = ShopProfile.objects.get(id=profile_id)
                if firstName is not None:
                    profile.first_name = firstName
                if lastName is not None:
                    profile.last_name = lastName
                if email is not None:
                    profile.user.email = email
                    profile.user.username = email
                if password:
                    profile.user.set_password(password)
                if avatar:
                    profile.avatar = avatar
                profile.save()
                profile.user.save()

                return Response(
                    {
                        "message": "Success. Profile for user ID: "
                        + str(profile_id)
                        + " updated."
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            except ObjectDoesNotExist:
                # in case if we manually create a new user, without creating profile
                if firstName is not None and lastName is not None:
                    user = CoreUser.objects.get(email=email)
                    ShopProfile.objects.create(
                        user=user,
                        first_name=firstName,
                        last_name=lastName,
                    )
                return Response(
                    {
                        "message": "Success. Profile for user ID: "
                        + str(profile_id)
                        + " created."
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError as e:
                if "unique constraint" in str(e).lower():
                    return Response(
                        {"error": "Email is already taken."},
                        status=status.HTTP_409_CONFLICT,
                    )
                return Response(
                    {"error": "Database error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        case "GET":
            try:
                profile = ShopProfile.objects.get(id=profile_id)
                serializer = ShopProfileSerializer(profile, many=False)
                serialized_data = serializer.data
                return Response(serialized_data)
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

        case "DELETE":
            try:
                user = CoreUser.objects.get(id=profile_id)
                profile = ShopProfile.objects.get(user=user)
                user.delete()
                profile.delete()
                return Response(
                    {"message": "Success. User " + str(profile_id) + " deleted."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@login_required()
def permission_get(request):
    if not can_view_groups(request.user):
        raise PermissionDenied("You don't have permission to view permissions.")
    required_perms = [
        "view_shopprofile",
        "change_shopprofile",
        "view_group",
        "change_group",
    ]
    permissions = Permission.objects.filter(codename__in=required_perms)
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@login_required()
def role_get(request):
    if not can_view_groups(request.user):
        raise PermissionDenied("You don't have permission to view groups.")
    roles = Group.objects.all()
    serializer = GroupSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@login_required()
@permission_required("auth.change_group", raise_exception=True)
def role_create(request):
    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@login_required()
def permission_user_get(request):
    permissions = list(request.user.get_all_permissions())
    return Response({"permissions": permissions}, status=status.HTTP_200_OK)


@api_view(["GET"])
@login_required()
def product_get(request, product_id=None):
    if not can_view_products(request.user):
        raise PermissionDenied("You don't have permission to view products.")
    if product_id:
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@login_required()
@permission_required("shop.change_product", raise_exception=True)
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, CanModifyOrViewOrder]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
