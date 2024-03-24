from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shop.models import Profile
from .serializers import ProfileSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
            "sorting": True
        },
        {
            "key": "role",
            "label": "Role",
            "sorting": True
        },
    ]

    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    serialized_data = serializer.data

    return Response({"headers": headers, "rows": serialized_data})