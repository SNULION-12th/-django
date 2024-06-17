from rest_framework.serializers import ModelSerializer
from account.serializers import UserIdUsernameSerializer #추가

from .models import Comment


class CommentSerializer(ModelSerializer):
    author = UserIdUsernameSerializer(read_only=True) #추가

    class Meta:
        model = Comment
        fields = "__all__"
