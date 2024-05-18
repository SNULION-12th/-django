from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Comment
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.models import User
from post.models import Post
from rest_framework.views import APIView
from drf_yasg import openapi

# Create your views here.
class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="해당 post의 모든 comments를 리턴합니다.",
        manual_parameters=[
            openapi.Parameter(
                'post',
                openapi.IN_QUERY,
                description="포스트 ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: CommentSerializer, 404: "Not Found"},
    )
    def get(self, request):
        post_id= request.GET.get('post')

        try:
            Post.objects.get(id = post_id)
        except:
            return Response(
                {"detail": "POST Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="새로운 코멘트를 남깁니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
    )
    def post(self, request):
        author_info = request.data.get("author")
        post_id = request.data.get('post')
        content = request.data.get('content')
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not post_id or not content:
            return Response(
                {"detail": "[post, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            comment = Comment.objects.create(post_id = post_id, content=content, author=author)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        comment.content = content
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)