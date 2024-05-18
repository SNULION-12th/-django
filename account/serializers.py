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
        fields = ["id", "username", "password", "email"] #--이 값들이 user 라는 것에 담길 것. 
        #firstname, lastname, 등 뭐가 많지만 그 중에 이것들만 사용할 것임.


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = "__all__"