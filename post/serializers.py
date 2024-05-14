from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True) #✏️serializer를 중첩해줘야 content 값을 가져올 수 있음
    class Meta:
        model = Post
        fields = "__all__"