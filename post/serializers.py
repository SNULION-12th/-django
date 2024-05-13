from rest_framework.serializers import ModelSerializer
from .models import Post
<<<<<<< HEAD
from tag.serializers import TagSerializer

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
=======

class PostSerializer(ModelSerializer):
>>>>>>> fb50bd764cbec7a56688593b44ce28f451dd53e0
    class Meta:
        model = Post
        fields = "__all__"