from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer,UserProfileSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.request_serializers import (
    SignInRequestSerializer,
    SignUpRequestSerializer,
    TokenRefreshRequestSerializer,
    SignOutSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


def generate_token_in_serialized_data(user, user_profile):
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token)
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data["token"] = {"access": access_token, "refresh": refresh_token}
    return serialized_data

def set_token_on_response_cookie(user, status_code):
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    serialized_data = UserProfileSerializer(user_profile).data
    res = Response(serialized_data, status=status_code)
    res.set_cookie("refresh_token", value=str(token), httponly=True)
    res.set_cookie("access_token", value=str(token.access_token), httponly=True)
    return res

class SignUpView(APIView):
    @swagger_auto_schema(
        operation_id="회원가입",
        operation_description="회원가입을 진행합니다.",
        request_body=SignUpRequestSerializer,
        responses={201: UserProfileSerializer, 400: "Bad Request"},
    )
    def post(self, request):

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user.password)
            user.save()
            
        college=request.data.get('college')
        major=request.data.get('major')
            
        user_profile = UserProfile.objects.create(
            user=user,
            college=college,
            major=major
        )
        return set_token_on_response_cookie(user, status_code=status.HTTP_201_CREATED)


class SignInView(APIView):
    @swagger_auto_schema(
        operation_id="로그인",
        operation_description="로그인을 진행합니다.",
        request_body=SignInRequestSerializer,
        responses={200: UserSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request):
        # query_params 에서 username, password를 가져온다.
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response(
                {"message": "missing fields ['username', 'password'] in query_params"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response(
                    {"message": "Password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return set_token_on_response_cookie(user, status_code=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

class TokenRefreshView(APIView):
    @swagger_auto_schema(
        operation_id="토큰 재발급",
        operation_description="access 토큰을 재발급 받습니다.",
        request_body=TokenRefreshRequestSerializer,
        responses={200: UserProfileSerializer},
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        #### 1
        if not refresh_token:
            return Response(
                {"detail": "no refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
        #### 2
            RefreshToken(refresh_token).verify()
        except:
            return Response(
                {"detail": "please signin again."}, status=status.HTTP_401_UNAUTHORIZED
            )
            
        #### 3
        new_access_token = str(RefreshToken(refresh_token).access_token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie("access_token", value=str(new_access_token), httponly=True)
        return response

class SignOutView(APIView):
    @swagger_auto_schema(
        operation_id="로그아웃",
        operation_description="로그아웃을 진행합니다.",
        request_body=SignOutSerializer,
        responses={200: "OK", 400: "Invalid Request", 401: "Unauthorized"},
    )
    def post(self, request):
        refresh_token = request.data.get("refreshToken")
        if not refresh_token:
            return Response(
                {"detail": "no refreshToken provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            is_blacklisted = BlacklistedToken.objects.filter(token__jti=token['jti']).exists()
            if is_blacklisted:
                return Response(
                    {"detail": "Token is already blacklisted."}, status=status.HTTP_400_BAD_REQUEST
                )
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Invalid token. Please sign in again."}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
