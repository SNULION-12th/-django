from rest_framework.serializers import ModelSerializer
from .models import Post, Comment
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"