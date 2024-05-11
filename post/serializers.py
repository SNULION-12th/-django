from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post

class PostSerializer(ModelSerializer): #이미 만들어진 ModelSerializer를 상속 받아서 사용
    tags = TagSerializer(many=True, read_only=True)
    #many=True 옵션을 통해 여러 태그에 대해서 직렬화해야할 수도 있다고 적기
    class Meta: #시리얼라이저에 전달해줄 모델의 메타데이터를 기술
        model = Post
        fields = "__all__"