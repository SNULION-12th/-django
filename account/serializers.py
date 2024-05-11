from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile


class UserIdUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True) #UserSerializer의 모든 내용이 적용됨 -> 외래키로 연결되는 모델을 쉽게 처리할 수 있음
    class Meta:
        model = UserProfile
        fields = "__all__"