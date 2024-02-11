from django.shortcuts import render
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post, Like, User
from tag.models import Tag
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema


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
            responses={200: PostSerializer(many=True)}
        )
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
        title = request.data.get('title')
        content = request.data.get('content')
        tag_contents = request.data.get("tags")
        author = User.objects.get(username=request.data.get('username'))

        if not author:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author.password != request.data.get('password'):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        post = Post.objects.create(title=title, content=content, author=author)
        
        if tag_contents is not None:
            for tag_content in tag_contents:
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
            responses={200: PostSerializer}
        )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(instance = post)
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
        
        author = User.objects.get(username=request.data.get('username'))
        
        if author.password != request.data.get('password'):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        if post.author != author:
            return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
            operation_id='게시글 수정',
            operation_description='게시글을 수정합니다. 과제로 구현할 부분입니다.',
            request_body=PostSerializer,
            responses={200: PostSerializer, 404: 'Not Found', 400: 'Bad Request'}
        )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        author = User.objects.get(username=request.data.get('username'))
        
        if author.password != request.data.get('password'):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        if post.author != author:
            return Response({"detail": "You are not the author of this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        post.title = title
        post.content = content
        post.save()
        serializer = PostSerializer(instance = post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeView(APIView):
    @swagger_auto_schema(
            operation_id='좋아요 토글',
            operation_description='좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.',
            request_body=PostSerializer,
            responses={200: PostSerializer, 404: 'Not Found'}
        )
    def post(self, request, post_id):

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        ### 2 ###
        try:
            author = User.objects.get(username=request.data.get('username'))
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author.password != request.data.get('password'):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
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