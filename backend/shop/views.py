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