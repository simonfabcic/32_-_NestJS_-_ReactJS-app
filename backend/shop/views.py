from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from math import ceil
from django.core.paginator import Paginator
from django.db import connection

from .serializers import ShopProfileSerializer

from shop.models import ShopProfile
from core.models import CoreUser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# URL: /profiles?offset=[int]&page_size=[int]&sort_by=[options]&sort_order=[asc|desc]
def getProfiles(request):
  headers = [
    {
      "key": "email",
      "label": "Email",
      "sorting": True
    },
    {
      "key": "full_name",
      "label": "Full name",
      "sorting": False
    },
    {
      "key": "role",
      "label": "Role",
      "sorting": True
    },
  ]

  for header in headers:
    if header["sorting"]:
      default_sort_by = header["key"]
      break
  
  offset = request.GET.get("offset", "5")
  page_size = request.GET.get("page_size", "15")
  sort_by = request.GET.get("sort_by", default_sort_by)
  sort_order = request.GET.get("sort_order", "ASCss")

  # print (
  # "offset: " + offset,
  # "page_size: " + page_size,
  # "sort_by: " + sort_by,
  # "sort_order: " + sort_order,
  # )

  # checking if URL parameters are OK
  if not (
      offset.isdigit() and
      page_size.isdigit() and
      any(header["key"] == sort_by for header in headers) and
      sort_order in ["ASC", "DESC"]):
    sortingOptions = ""
    for header in headers:
      if len(sortingOptions) > 0:
        sortingOptions += "|"
      sortingOptions =  sortingOptions + header["key"]
    options = "/profiles?offset=[int]&page_size=[int]&sort_by=[" + sortingOptions + "]&sort_order=[asc|desc]"
    return Response({"error":"Error in parameters.", "options":options}, status=status.HTTP_400_BAD_REQUEST)
  
  offset = int(offset)
  page_size = int(page_size)

  profiles = ShopProfile.objects.all()

  # total_records = profiles.count()
  # total_pages = ceil(total_records / page_size) # round up with 'ceil'
  current_page = (offset / page_size) + 1
  # prev_page = current_page - 1 if current_page > 1 else None
  # next_page = current_page + 1 if current_page < total_pages else None

  # https://docs.djangoproject.com/en/5.0/topics/pagination/
  p = Paginator(profiles, page_size)
  try:
    page = p.page(current_page)
  except:
    return Response({"error":"Parameters 'offset' and 'page_size' not compatible"}, status=status.HTTP_400_BAD_REQUEST)



  serializer = ProfileSerializer(page.object_list, many=True)
  serialized_data = serializer.data

  pagination_description = [
    {
      "sort_order": sort_order,
      "sort_by": sort_by,
      "total_records": p.count,
      "total_pages": p.num_pages,
      "current_page": current_page,
      "prev_page": page.previous_page_number() if page.has_previous() else None,
      "next_page": page.next_page_number() if page.has_next() else None,
      "page_size": page_size,
    }
  ]
  return Response({"headers": headers, "rows": serialized_data, "pagination_description": pagination_description}, status=status.HTTP_200_OK)

@api_view(['POST'])
def profileNew(request):
  firstName = request.data.get("firstName")
  lastName = request.data.get("lastName")
  email = request.data.get("email")
  password = request.data.get("password")
  if not (firstName and lastName and email and password):
    return Response({"message":"Fail. Profile not created."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
  try:
    user = CoreUser.objects.create_user(
    username=email,
    email=email,
    password=password)
    profile = ShopProfile.objects.create(
      user = user,
      first_name = firstName,
      last_name = lastName,
      # role = Role.objects.get(name=random.choice(ROLES)) # TODO add role
    )
    return Response({"message":"Success. Profile created."}, status=status.HTTP_201_CREATED)  
  except IntegrityError:
    return Response({"error": "Email already taken."}, status=status.HTTP_409_CONFLICT)
  except:
    return Response({"error":"Error creating new user."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, profile_id):
  match request.method:
    case 'PUT':
      firstName = request.data.get("firstName")
      lastName = request.data.get("lastName")
      email = request.data.get("email")
      password = request.data.get("password")
      userID = request.data.get("userID")
      try:
        profile = ShopProfile.objects.get(id=profile_id)
        if firstName is not None: profile.first_name = firstName
        if lastName is not None: profile.last_name = lastName
        if email is not None: profile.user.email = email
        if password is not None: profile.user.password = password
        profile.save()
        return Response({"message":"Success. Profile for user ID: " + str(profile_id) + " updated."}, status=status.HTTP_204_NO_CONTENT)
      except ObjectDoesNotExist:
        # in case if we manually create a new user, without creating profile
        # QUESTION why this does not work for admin (with pk = 1)
        if firstName is not None and lastName is not None:
          user = CoreUser.objects.get(pk=int(userID))
          ShopProfile.objects.create(
            user = user,
            first_name = firstName,
            last_name = lastName,
          )
        return Response({"message":"Success. Profile for user ID: " + str(profile_id) + " created."}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    case 'GET':
      try: 
        profile = ShopProfile.objects.get(id=profile_id)
        serializer = ProfileSerializer(profile, many=False)
        serialized_data = serializer.data
        return Response(serialized_data)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_404_NOT_FOUND)

    case 'DELETE':
      # profile = Profile.objects.delete(user__username=username)
      try:
        user = CoreUser.objects.get(id=profile_id)
        # profile = Profile.objects.get(user__id=user_id)
        profile = ShopProfile.objects.get(user=user)
        user.delete()
        profile.delete()
        return Response({"message":"Success. User " + str(profile_id) + " deleted."}, status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_404_NOT_FOUND)