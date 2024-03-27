from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

@api_view(['POST', 'PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, username):
  match request.method:
    case 'POST':
      user = User.objects.create_user(
        username='john',
        email='jlennon@beatles.com',
        password='glass onion')
      profile = Profile()
      profile.user
    case 'PUT':
      pass
    case 'GET':
      profile = Profile.objects.get(user__username=username)
      serializer = ProfileSerializer(profile, many=False)
      serialized_data = serializer.data
      return Response(serialized_data)
    case 'DELETE':
      # profile = Profile.objects.delete(user__username=username)
      try:
        profile = Profile.objects.get(user__username=username)
        profile.delete()
        return Response({"message":"Success. User " + str(username) + " deleted."}, status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
        return Response({"message":str(e)}, status=status.HTTP_404_NOT_FOUND)