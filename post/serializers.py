from rest_framework.serializers import ModelSerializer
from .models import Post

class PostSerializer(ModelSerializer): #이미 만들어진 ModelSerializer를 상속 받아서 사용
    class Meta: #시리얼라이저에 전달해줄 모델의 메타데이터를 기술
        model = Post
        fields = "__all__"