from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagSerializer

from post.models import Post
from post.serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema


class TagListView(APIView):
  @swagger_auto_schema(
    operation_id='태그 목록 조회',
    operation_description='태그 목록을 조회합니다.',
    responses={200: TagSerializer(many=True)}
  )
  def get(self, request): #그냥 모든 태그들의 목록을 조회하는 api
    tags = Tag.objects.all()
    serializer = TagSerializer(instance=tags, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    operation_id='태그 생성',
    operation_description='태그를 생성합니다.',
    request_body=TagSerializer,
    responses={201: TagSerializer}
  )
  def post(self, request):
    content = request.data.get('content') #요청에서 태그의 내용을 뽑아냄
    
    if not content: #태그의 내용이 없다면 에러 리턴
      return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

    if Tag.objects.filter(content=content).exists(): #태그 db에서 태그의 내용과 같은 객체가 있다면 이미 존재하므로 생성불가 에러 리턴
      return Response({"detail" : "Tag with same content already exists"}, status=status.HTTP_409_CONFLICT)

    tag = Tag.objects.create(content=content) #태그 내용을 넣어서 태그 객체 생성후 db에 등록
    serializer = TagSerializer(instance = tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED) # 직렬화 해서 data만 응답으로 넘겨줌 
 
 
class TagDetailView(APIView):
  
  @swagger_auto_schema(
    operation_id='태그 내부 게시물 조회',
    operation_description='해당 태그가 달린 게시물을 조회합니다.',
    responses={200: PostSerializer(many=True), 204: 'No Content'}
  )
  def get(self, request, tag_id):
    try:
      Tag.objects.get(id=tag_id) #태그 아이디에 맞는 태그 객체를 뽑아옴 
    except: #없을 경우 에러 리턴
      return Response({"detail": "Provided tag does not exist."}, status=status.HTTP_204_NO_CONTENT)
    
    posts = Post.objects.filter(tags=tag_id) #게시물 중 해당 태그를 가진 게시물 객체를 뽑아옴
    serializer = PostSerializer(instance=posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) #직렬화해서 data만 응답으로 넘겨줌