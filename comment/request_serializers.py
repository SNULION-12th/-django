from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer


class ComentListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    post = serializers.IntegerField()
    content = serializers.CharField()


class ComentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()
