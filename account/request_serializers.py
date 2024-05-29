### 🔻 이 부분 추가 🔻 ###
from rest_framework import serializers


class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    college = serializers.CharField()
    major = serializers.CharField()


class SignInRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

### 🔺 이 부분 추가 🔺 ###

class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class LogOutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()