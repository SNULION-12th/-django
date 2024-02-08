from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer

from post.models import Post
from post.serializers import PostSerializer


class TagListView(APIView):
  def get(self, request):
    tags = Tag.objects.all()
    serializer = TagSerializer(instance=tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    content = request.data.get('content')
    
    if not content:
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    if Tag.objects.filter(content=content).exists():
      return Response({"detail" : "Tag with same content already exists"}, status=status.HTTP_409_CONFLICT)

    tag = Tag.objects.create(content=content)
    serializer = TagSerializer(tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class TagDetailView(APIView):
  def get(self, request, tag_id):
    try:
      Tag.objects.get(id=tag_id)
    except:
      return Response({"detail": "Provided tag does not exist."})
    
    posts = Post.objects.filter(tags=tag_id)
    serializer = PostSerializer(instance=posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)