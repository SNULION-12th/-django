from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, User

from .models import Comment
from .serializers import CommentSerializer
from account.serializers import UserBasicSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id='댓글 목록 조회',
        operation_description='특정 게시글의 댓글 목록을 조회합니다.',
        manual_parameters=[
            openapi.Parameter(
                'post',
                openapi.IN_QUERY,
                description='게시글 id',
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: CommentSerializer(many=True), 404: 'Not Found'}
    )
    def get(self, request):
        post_id = request.query_params.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post'] in query params"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id='댓글 생성',
        operation_description='특정 게시글에 댓글을 생성합니다.',
        request_body=CommentSerializer,
        responses={201: CommentSerializer, 400: 'Bad Request', 404: 'Not Found', 403: 'Forbidden'}
    )
    def post(self, request):
        author_request = request.data.get("author")
        if not author_request:
            return Response({"detail": "missing fields ['author']"}, status=status.HTTP_400_BAD_REQUEST)
        username = author_request.get('username')
        password = author_request.get('password')
        post_id = request.data.get('post')
        content = request.data.get('content')
        if not username or not password:
            return Response({"detail": "missing fields ['username', 'password']"}, status=status.HTTP_400_BAD_REQUEST)
        if not post_id or not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response({"detail": "Password is wrong!"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = Comment.objects.create(post_id=post_id, author=author, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id='댓글 수정',
        operation_description='특정 댓글을 수정합니다.',
        request_body=CommentSerializer,
        responses={200: CommentSerializer, 400: 'Bad Request', 404: 'Not Found', 401: 'Unauthorized'}
    )
    def patch(self, request, comment_id):
        content = request.data.get('content')
        author_request = request.data.get("author")
        if not author_request or not content:
            return Response({"detail": "missing fields ['author', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        username = author_request.get('username')
        password = author_request.get('password')
        if not username or not password:
            return Response({"detail": "missing fields ['username', 'password']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response({"detail": "Password is wrong!"}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment.content = content
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id='댓글 삭제',
        operation_description='특정 댓글을 삭제합니다.',
        request_body=UserBasicSerializer,
        responses={204: 'No Content', 400: 'Bad Request', 404: 'Not Found', 401: 'Unauthorized'}
    )
    def delete(self, request, comment_id):

        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"detail": "missing fields ['username', 'password']"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response({"detail": "Password is wrong!"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if author != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        