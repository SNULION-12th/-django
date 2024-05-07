from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema

# 각 view마다 주소를 다르게 해주어야 함
# 이 view는 url에 따로 숫자가 붙지 않아서 올 것임
class PostListView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={200: PostSerializer(many=True)}
        )
      
		### 얘네가 class inner function 들! ###
    def get(self, request): 
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer}
        )

    def post(self, request):
        # user가 보낸 request에서 정보를 잡는 것
        title = request.data.get('title')
        content = request.data.get('content')
        # if는 예외처리: 만약 title, content가 없을 경우 error을 뱉겠다는 것!
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        return Response({
            "id":post.id,
            "title":post.title,
            "content":post.content,
            "created_at":post.created_at
            }, status=status.HTTP_201_CREATED)

# 이 class는 url마다 숫자가 다르게 붙어서 올 것임
class PostDetailView(APIView):
    def get(self, request, post_id):
        # post_id가 성공하면 넘어가고, 없으면 except 에러_"그런 거 없어"_를 내뱉을 예정
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({
        #     "id":post.id,
        #     "title":post.title,
        #     "content":post.content,
        #     "created_at":post.created_at
        #     }, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        # 먼저 그 포스트가 있는지 확인
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        # 삭제를 성공한 것이라 'No content'
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        post.title = request.data.get("title")
        post.content = request.data.get("content")
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)