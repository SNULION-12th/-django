from rest_framework.serializers import ModelSerializer
from account.serializers import UserBasicSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["post","content","author"]
        exatra_kwargs = {"post":{"required":True},"content":{"required":True}}