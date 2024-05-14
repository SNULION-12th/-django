from rest_framework.serializers import ModelSerializer
from .models import Post
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    #-- 여기서 serializer 중첩을 해줘야 tag의 id 뿐만 아니라 content도 가져올 수 있다. tag id 만 가져왔기 때문에 tag content 를 가져오려면 tag 모델을 해석할 또 다른 번역기가 필요한 느낌(?)
    class Meta:
        model = Post
        fields = "__all__"