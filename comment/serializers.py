from rest_framework.serializers import ModelSerializer
from comment.models import Comment

class commentSerializer(ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"