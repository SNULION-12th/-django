from rest_framework.serializers import ModelSerializer
from .models import Comment
from post.serializers import PostSerializer
from account.serializers import UserSerializer


class CommentCreateSerializer(ModelSerializer):
  author = UserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = ["author", "post", "content"]

class CommentSerializer(ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"

class CommentUpdateSerializer(ModelSerializer):
  author = UserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = ["author", "content"]

class CommentDeleteSerializer(ModelSerializer):
  author = UserSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = ["author"]