from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserIdUsernameSerializer, UserSerializer, UserProfileSerializer
from .models import UserProfile

class AccountView(APIView):
    @swagger_auto_schema(
        operation_id='회원가입',
        operation_description='회원가입을 진행합니다.',
        request_body=UserProfileSerializer,
        responses={201: UserProfileSerializer}
    )
    def post(self, request):
        college=request.data.get('college')
        major=request.data.get('major')
        
        if not college or not major:
            return Response({"message": "missing fields ['college', 'major']"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        ) 
        user_profile_serializer = UserProfileSerializer(instance = user_profile)
        return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_id='로그인',
        operation_description='로그인을 진행합니다.',
        request_body=UserSerializer,
        responses={200: UserSerializer}
    )
    def get(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            if not user.check_password(request.data.get('password')):
                return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user_serializer = UserSerializer(instance = user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        