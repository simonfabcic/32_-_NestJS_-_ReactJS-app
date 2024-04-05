from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .serializers import ProfileSerializer

from shop.models import Profile
from core.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request):
  headers = [
    {
      "key": "email",
      "label": "Email",
      "sorting": False
    },
    {
      "key": "full_name",
      "label": "Full name",
      "sorting": True
    },
    {
      "key": "role",
      "label": "Role",
      "sorting": True
    },
  ]

  pagination = [ # TODO
    {
      "key": "maintenance_date",
      "label": "Datum vzdrževanja",
      "prev_page": "/api/posts?offset=0&limit=10", # /* or "prev_page": 1 */
      "next_page": "/api/posts?offset=30&limit=10", # /* or "next_page": 3 */
      "current_page": 2,
      "page_size": 10,
      "total_records": 100,
      "total_pages": 10
    }
  ]

  profiles = Profile.objects.all()
  serializer = ProfileSerializer(profiles, many=True)
  serialized_data = serializer.data
  return Response({"headers": headers, "rows": serialized_data})

@api_view(['POST'])
def profileNew(request):
  firstName = request.data.get("firstName")
  lastName = request.data.get("lastName")
  email = request.data.get("email")
  password = request.data.get("password")
  if not (firstName and lastName and email and password):
    return Response({"message":"Fail. Profile not created."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
  try:
    user = User.objects.create_user(
    username='user',
    email=email,
    password=password)
    profile = Profile.objects.create(
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
        profile = Profile.objects.get(id=profile_id)
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
          user = User.objects.get(pk=int(userID))
          Profile.objects.create(
            user = user,
            first_name = firstName,
            last_name = lastName,
          )
        return Response({"message":"Success. Profile for user ID: " + str(profile_id) + " created."}, status=status.HTTP_201_CREATED)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    case 'GET':
      try: 
        profile = Profile.objects.get(id=profile_id)
        serializer = ProfileSerializer(profile, many=False)
        serialized_data = serializer.data
        return Response(serialized_data)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_404_NOT_FOUND)

    case 'DELETE':
      # profile = Profile.objects.delete(user__username=username)
      try:
        user = User.objects.get(id=profile_id)
        # profile = Profile.objects.get(user__id=user_id)
        profile = Profile.objects.get(user=user)
        user.delete()
        profile.delete()
        return Response({"message":"Success. User " + str(profile_id) + " deleted."}, status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_404_NOT_FOUND)