from rest_framework.serializers import ModelSerializer
from .models import Post

# 편하게 serialize할 수 있는 것을 이미 Django에서 가지고 있음
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        # 모델 전부를 쓸 것이라는 것
        fields = "__all__"
    