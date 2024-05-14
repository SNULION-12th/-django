### 🔻 이 부분 추가 🔻 ###
from rest_framework.serializers import ModelSerializer
from .models import Tag

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"