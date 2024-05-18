from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer


class PostListRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class PostDetailRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())