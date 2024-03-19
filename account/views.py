from django.contrib.auth.models import User 
from django.contrib import auth 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserIdUsernameSerializer, UserSerializer, UserProfileSerializer, UserBasicSerializer
from .models import UserProfile

class SignUpView(APIView):
    @swagger_auto_schema(
        operation_id='회원가입',
        operation_description='회원가입을 진행합니다.',
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: 'Bad Request'}
    )
    def post(self, request):
        profile = request.data.get('profile')
        
        if profile is None:
            return Response({"message": "missing fields ['profile']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if profile.get('college') is None or profile.get('major') is None:
            return Response({"message": "missing fields ['college', 'major'] in profile"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user.password)
            user.save()
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=profile.get('college'),
            major=profile.get('major')
        ) 
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    
class SignInView(APIView):
    @swagger_auto_schema(
        operation_id='로그인',
        operation_description='로그인을 진행합니다.',
        request_body=UserBasicSerializer,
        responses={200: UserSerializer, 404: 'Not Found', 400: 'Bad Request'}
    )
    def post(self, request):
        #query_params 에서 username, password를 가져온다.
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({"message": "missing fields ['username', 'password'] in query_params"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"message": "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            user_serializer = UserSerializer(instance = user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        