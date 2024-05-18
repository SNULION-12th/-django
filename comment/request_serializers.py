from rest_framework import serializers

from account.request_serializers import SignInRequestSerializer

class CommentListRequestSerializer(serializers.Serializer):
    content = serializers.CharField()
    post = serializers.IntegerField()
    author = SignInRequestSerializer()

class CommentDetailRequestSerializer(serializers.Serializer):
    content = serializers.CharField()
    author = SignInRequestSerializer()
