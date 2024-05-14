from rest_framework import serializers
from post.request_serializers import PostDetailRequestSerializer

class CommentListRequestSerializer(serializers.Serializer):
  postId = serializers.CharField()