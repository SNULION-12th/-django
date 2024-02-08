from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserIdUsernameSerializer, UserSerializer, UserProfileSerializer
from .models import UserProfile

class AccountView(APIView):
    def post(self, request):
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
    
    def get(self, request):
        user = User.objects.get(username = request.data.get('username'))
        if user is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get('password') != user.password:
            return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)