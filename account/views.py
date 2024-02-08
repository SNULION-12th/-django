from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserIdUsernameSerializer, UserSerializer, UserProfileSerializer
from .models import UserProfile

class SignupView(APIView):
    def post(self, request):
        print(request.user)
        college=request.data.get('college')
        major=request.data.get('major')

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        ) 
        user_profile_serializer = UserProfileSerializer(user_profile)
        res = Response(user_profile_serializer.data, status=status.HTTP_200_OK)
        return res