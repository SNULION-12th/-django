from django.shortcuts import render
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post

class PostListView(APIView):
		### 얘네가 class inner function 들! ###
     @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={200: PostSerializer(many=True)}
        )
     def get(self, request): 
        posts = Post.objects.all()
        contents = [{"id":post.id,
                     "title":post.title,
                     "content":post.content,
                     "created_at":post.created_at
                     } for post in posts]
        return Response(contents, status=status.HTTP_200_OK)
        
     @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer}
        )
     def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)