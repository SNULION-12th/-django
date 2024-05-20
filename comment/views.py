from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from post.models import Post
from drf_yasg.utils import swagger_auto_schema
from account.models import User
from drf_yasg import openapi

class CommentListView(APIView):
    def get(self, request):
        try: 
            post_id = request.GET.get('post')
            Post.objects.get(id = post_id)
            comments = Comment.objects.filter(post=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response({"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        author = request.user
        post_id = request.data.get("post")
        content = request.data.get("content")
        if not post_id or not content:
            return Response(
                 {"detail": "[content] fields missing."},
                 status=status.HTTP_400_BAD_REQUEST,
             )
        if not Post.objects.filter(id=post_id).exists():
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment = Comment.objects.create(
            post_id=post_id, author=author, content=content
        )

        serializer = CommentSerializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
    def put(self, request, comment_id):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        author = request.user
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
    operation_description="특정 댓글을 삭제합니다.",
    responses={
        204: "No Content",
        400: "Bad Request",
        404: "Not Found",
        401: "Unauthorized",
    },
    manual_parameters=[openapi.Parameter("Authorization", openapi.IN_HEADER, description="access token", type=openapi.TYPE_STRING)]
)
def delete(self, request, comment_id):
    if not request.user.is_authenticated:
        return Response(
            {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
        )
    author = request.user
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
            
