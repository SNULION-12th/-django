from rest_framework.serializers import ModelSerializer
from .models import Post
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    #-- 여기서 serializer 중첩을 해줘야 tag의 id 뿐만 아니라 content도 가져올 수 있다.
    class Meta:
        model = Post
        fields = "__all__"