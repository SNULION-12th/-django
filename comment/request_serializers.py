from rest_framework import serializers
from account.request_serializers import SignInRequestSerializer
from post.serializers import PostSerializer

class CommentRequestSerializer(serializers.Serializer):
    author = SignInRequestSerializer()
    content = serializers.CharField()
    post = serializers.IntegerField()