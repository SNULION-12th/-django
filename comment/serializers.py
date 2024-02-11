from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post","content","author","created_at"]
        exatra_kwargs = {"post":{"required":True},"content":{"required":True}}