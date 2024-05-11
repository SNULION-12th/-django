from rest_framework import serializers


class SignUpRequestSerializer(serializers.Serializer):  #회원가입할 때 받아야 하는 정보
    email = serializers.EmailField()
    password = serializers.CharField()
    username = serializers.CharField()
    college = serializers.CharField()
    major = serializers.CharField()


class SignInRequestSerializer(serializers.Serializer): #로그인할 때 받아야 하는 정보
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()