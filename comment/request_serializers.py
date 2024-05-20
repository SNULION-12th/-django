from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer


class CommentListRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    post = serializers.IntegerField()
    content = serializers.CharField()


class CommentDetailRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()
