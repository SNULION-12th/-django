from rest_framework.serializers import ModelSerializer
from .models import Post
from tag.serializers import TagSerializer
from account.serializers import UserIdUsernameSerializer

class PostSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
