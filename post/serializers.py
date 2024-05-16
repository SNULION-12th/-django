from rest_framework.serializers import ModelSerializer
from .models import Post
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class PostSerializer(ModelSerializer):
		### 🔻 이 부분 추가 🔻 ###
    tags = TagSerializer(many=True, read_only=True)
		### 🔺 이 부분 추가 🔺 ###
    class Meta:
        model = Post
        fields = "__all__"