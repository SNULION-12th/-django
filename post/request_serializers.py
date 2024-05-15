from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer


class PostListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class PostDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    title = serializers.CharField()
    content = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())


class CommentListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    post = serializers.CharField()
    content = serializers.CharField()

class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()