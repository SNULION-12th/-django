from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from account.models import User
from post.models import Post
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentListView(APIView):

    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="댓글을 조회합니다.",
        manual_parameters=[
        openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="post id",
            type=openapi.TYPE_INTEGER
        ),
    ],
        responses={200: CommentSerializer, 404: "Not Found"},)

    def get(self, request,):
        postId= request.GET.get('post')
        try:
            Post.objects.get(id=postId)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(post_id=postId)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
        manual_parameters=[openapi.Parameter("Authorization", openapi.IN_HEADER, description="access token", type=openapi.TYPE_STRING)],)

    def post(self, request):
        ### 🔻 이 부분 수정 🔻 ###
        if not request.user.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        author = request.user
        ### 🔺 이 부분 수정 🔺 ###
        post_id = request.data.get("post")
        content = request.data.get("content")

        if not post_id or not content:
            return Response(
                {"detail": "missing fields ['post', 'content']"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Post.objects.filter(id=post_id).exists():
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment = Comment.objects.create(
            post_id=post_id, author=author, content=content
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200:CommentSerializer , 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
        manual_parameters=[openapi.Parameter("Authorization", openapi.IN_HEADER, description="access token", type=openapi.TYPE_STRING)])

    def put(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        author = request.user
        ### 🔺 이 부분 수정 🔺 ###
        content = request.data.get("content")

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if author != comment.author:
            return Response(
                {"detail": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.content = content
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
        manual_parameters=[openapi.Parameter("Authorization", openapi.IN_HEADER, description="access token", type=openapi.TYPE_STRING)],)

    def delete(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        author = request.user
        ### 🔺 이 부분 수정 🔺 ###

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if author != comment.author:
            return Response(
                {"detail": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)