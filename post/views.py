from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema

class PostListView(APIView):
	### 얘네가 class inner function 들! ###
    @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={200: PostSerializer(many=True)}
        )
    def get(self, request): 
        # Post의 오브젝트를 모두 가져오기
        posts = Post.objects.all()
        # # 가져온 것들을 리스트로 만들어줌
        # contents = [{"id":post.id,
        #              "title":post.title,
        #              "content":post.content,
        #              "created_at":post.created_at
        #              } for post in posts]
        # # 데이터와 상태코드를 응답
        # return Response(contents, status=status.HTTP_200_OK)
        # serializer 사용
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer}
        )
    def post(self, request):
        # 요청 바디를 통해 들어온 데이터를 가져옴
        title = request.data.get('title')
        content = request.data.get('content')
        # 예외처리 title이나 content가 없을 때 
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        # 새로운 post 객체를 만들기
        post = Post.objects.create(title=title, content=content)
        # # 새롭게 만든 post 객체를 응답해준다.
        # return Response({
        #     "id":post.id,
        #     "title":post.title,
        #     "content":post.content,
        #     "created_at":post.created_at
        #     }, status=status.HTTP_201_CREATED)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostDetailView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            responses={200: PostSerializer}
        )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # return Response({
        #     "id":post.id,
        #     "title":post.title,
        #     "content":post.content,
        #     "created_at":post.created_at
        #     }, status=status.HTTP_200_OK)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
            operation_id='게시글 삭제',
            operation_description='게시글을 삭제합니다.',
            responses={204: 'No Content', 404: 'Not Found'}
        )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)