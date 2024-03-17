from rest_framework.serializers import ModelSerializer
from .models import Post
from account.serializers import  UserBasicSerializer
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    
    author = UserBasicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"