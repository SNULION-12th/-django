from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from comment.models import Comment
from account.models import User
from .request_serializers import CommentRequestSerializer
from .serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

from drf_yasg import openapi

post_param = openapi.Parameter(
    'post',
    openapi.IN_QUERY,
    description="게시글 id",
    type=openapi.TYPE_INTEGER
)

class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="게시글에 댓글을 생성합니다.",
        request_body=CommentRequestSerializer,
        responses={201: "Created", 400: "missing field", 403: "password wrong", 404: "Not Found"},
    )
    def post(self, request):
        author_info = request.data.get("author")
        postId = request.data.get("post")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        if not postId:
            return Response(
                {"detail": "post field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = Post.objects.get(id=postId)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        
        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = Comment.objects.create(content=content, post=post, author=author)
        return Response(status=status.HTTP_201_CREATED)
    

    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="게시글에 달린 댓글을 조회합니다.",
        responses={200: "OK", 404: "Not Found"},
        manual_parameters=[post_param]
    )
    def get(self, request):
        postId = request.GET.get("post", None)
        try:
            post = Post.objects.get(id=postId)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        comments = post.comment_set.all()
        return Response(
            {"comments": [{"content": comment.content, "author": comment.author.username} for comment in comments]},
            status=status.HTTP_200_OK
        )

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="게시글에 달린 댓글을 수정합니다.",
        request_body=CommentRequestSerializer,
        responses={200: "OK", 400: "missing field", 403: "password wrong or No authorization of comment", 404: "Not Found"},
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
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
            )

        comment.content = content
        comment.save()
        return Response(status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="게시글에 달린 댓글을 삭제합니다.",
        responses={204: "No Content", 404: "missing field or no comment", 403: "password wrong or No authorization of comment"},
    )
    def delete(self, request, comment_id):
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
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="게시글에 달린 댓글을 조회합니다.",
        responses={200: "OK", 404: "Not Found"},
    )
    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"content": comment.content, "author": comment.author.username},
            status=status.HTTP_200_OK
        )