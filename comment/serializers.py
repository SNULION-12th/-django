from rest_framework.serializers import ModelSerializer
from .models import Comment

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        
        
class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"