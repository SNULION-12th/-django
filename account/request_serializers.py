from rest_framework import serializers

#요청을 처리하는 serializer 만들기

class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    college = serializers.CharField()
    major = serializers.CharField()


class SignInRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class TokenRefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class SignOutReqeustSerializer(serializers.Serializer):
    refresh = serializers.CharField()