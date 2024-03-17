from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post, Like, User
from tag.models import Tag
from .serializers import PostSerializer
from account.serializers import UserBasicSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# FBV는 토글 내부 내용에서 확인 가능
# @api_view(['POST'])
# def CreatePostView(request):
#     title = request.data.get('title')
#     content = request.data.get('content')
#     post = Post.objects.create(title=title, content=content)
#     return Response({"msg":f"'{post.title}'이 생성되었어요!"})

# @api_view(['GET'])
# def ReadAllPostView(request):
#     posts = Post.objects.all()
#     contents = [{post.title:post.content} for post in posts]
#     return Response({"posts":contents})

class PostListView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            manual_parameters=[
                openapi.Parameter('username', openapi.IN_QUERY, description="게시글 작성자의 username", type=openapi.TYPE_STRING, required=True),
                openapi.Parameter('password', openapi.IN_QUERY, description="게시글 작성자의 password", type=openapi.TYPE_STRING, required=True),
            ],
            responses={200: PostSerializer(many=True), 404: 'Not Found', 400: 'Bad Request'}
        )
    def get(self, request): 
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        if username is None or password is None:
            return Response({"detail": "username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        posts = Post.objects.filter(author__username=username)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer, 404: 'Not Found', 400: 'Bad Request'}
        )
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        tag_contents = request.data.get("tags")
        author_request = request.data.get('author')
        if not author_request:
            return Response({"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST)
        username = author_request.get('username')
        password = author_request.get('password')
        if not username or not password:
                return Response({"detail": "[username, password] fields missing in author"}, status=status.HTTP_400_BAD_REQUEST)
        if not title or not content:
                return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            post = Post.objects.create(title=title, content=content, author=author)
        except:
            return Response({"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if tag_contents is not None:
            for tag_content_j in tag_contents:
                tag_content = tag_content_j.get('content')
                if not tag_content:
                    return Response({"detail": "content field missing in tags"}, status=status.HTTP_400_BAD_REQUEST)
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
            
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            manaual_parameters=[
                openapi.Parameter('username', openapi.IN_QUERY, description="게시글 작성자의 username", type=openapi.TYPE_STRING, required=True),
                openapi.Parameter('password', openapi.IN_QUERY, description="게시글 작성자의 password", type=openapi.TYPE_STRING, required=True),
            ],
            responses={200: PostSerializer,400: 'Bad Request'}
        )
    def get(self, request, post_id):
        if not request.query_params.get('username') or not request.query_params.get('password'):
            return Response({"detail": "username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if post.author.username != request.query_params.get('username'):
            return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)
        if not post.author.check_password(request.query_params.get('password')):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(instance = post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
            operation_id='게시글 삭제',
            operation_description='게시글을 삭제합니다.',
            request_body=UserBasicSerializer,
            responses={204: 'No Content', 404: 'Not Found', 400: 'Bad Request'}
        )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            author = User.objects.get(username=request.data.get('username'))
            if not author.check_password(request.data.get('password')):
                return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            if post.author != author:
                return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
            operation_id='게시글 수정',
            operation_description='게시글을 수정합니다.',
            request_body=PostSerializer,
            responses={200: PostSerializer, 404: 'Not Found', 400: 'Bad Request'}
        )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        author_request = request.data.get('author')
        if not author_request:
            return Response({"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST)
        username = author_request.get('username')
        password = author_request.get('password')
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            if post.author != author:
                return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post.title = title
        post.content = content
        
        tag_contents = request.data.get("tags")
        if tag_contents is not None:
            post.tags.clear()
            for tag_content_j in tag_contents:
                tag_content = tag_content_j.get('content')
                if not tag_content:
                    return Response({"detail": "content field missing in tags"}, status=status.HTTP_400_BAD_REQUEST)
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        post.save()
        serializer = PostSerializer(instance = post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LikeView(APIView):
    @swagger_auto_schema(
            operation_id='좋아요 토글',
            operation_description='좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.',
            request_body=UserBasicSerializer,
            responses={200: PostSerializer, 404: 'Not Found', 400: 'Bad Request'}
        )
    def post(self, request, post_id):

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        ### 2 ###
        try:
            author = User.objects.get(username=request.data.get('username'))
            if not author.check_password(request.data.get('password')):
                return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        ### 3 ###
        like_list = post.like_set.filter(user=author)

        ### 4 ###
        if like_list.count() > 0:
            post.like_set.get(user=author).delete()
            print("좋아요 취소")
        else:
            Like.objects.create(user=author, post=post)
            print("좋아요 누름")

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)