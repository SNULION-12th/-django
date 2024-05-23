from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from post.models import Post
from account.models import User
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="댓글 목록을 조회합니다.",
        manual_parameters=[
            openapi.Parameter(
                'post',
                openapi.IN_QUERY,
                description="Post ID to filter comments",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
        },
    )
    def get(self, request):
        post_id = request.GET.get("post")
        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post=post_id).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_id="댓글 작성",
        operation_description="댓글을 작성합니다.",
        request_body=CommentListRequestSerializer,
        responses={
            201: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def post(self, request):
        post_id = request.data.get("post")
        author_info = request.data.get("author")
        content = request.data.get("content")

        if not author_info:
            return Response({"detail": "author field missing"}, status=status.HTTP_400_BAD_REQUEST)

        username = author_info.get("username")
        password = author_info.get("password")

        if not username or not password:
            return Response({"detail": "[username, password] fields missing in author"}, status=status.HTTP_400_BAD_REQUEST)

        if not post_id:
            return Response({"detail": "Post field missing"}, status=status.HTTP_400_BAD_REQUEST)

        if not content:
            return Response({"detail": "Content field missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            author = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if not author.check_password(password):
            return Response({"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)

        comment = Comment.objects.create(post=post, content=content, author=author)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 상세 조회",
        operation_description="댓글을 상세 조회합니다.",
        responses={
            200: CommentSerializer,
            404: "Not Found",
        },
    )
    def get(self, request, commentId):
        if not Comment.objects.filter(id=commentId).exists():
            return Response({"detail": "Comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
        comment = Comment.objects.get(id=commentId)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def put(self, request, commentId):
        author = request.data.get("author")
        content = request.data.get("content")

        if not author or not content:
            return Response({"detail": "[author, content] fields missing"}, status=status.HTTP_400_BAD_REQUEST)

        username = author.get("username")
        password = author.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"detail": "Wrong Password"}, status=status.HTTP_403_FORBIDDEN)

        try:
            comment = Comment.objects.get(id=commentId)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.author != user:
            return Response({"detail": "Unauthorized Comment"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.content = content
        comment.save()

        comment_serializer = CommentSerializer(instance=comment)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={
            204: "No Content",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def delete(self, request, commentId):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "[username, password] field missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"detail": "Wrong Password"}, status=status.HTTP_403_FORBIDDEN)

        try:
            comment = Comment.objects.get(id=commentId)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.author != user:
            return Response({"detail": "Unauthorized Comment"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
