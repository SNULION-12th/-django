from django.shortcuts import render
#rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
##필요한 것들
from .models import Comment
from .serializers import CommentSerializer
from post.models import Post
from account.models import User
from .request_serializer import CommentListRequestSerializer, CommentDetailRequestSerializer
##swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class CommentListView(APIView): ##get, create
  #TO DO 1 (get 구현)

  def get(self, request, post_id):
    try:
      Post.objects.get(id=post_id)
    except:
      return Response({"detail": "wrong post id."}, status=status.HTTP_404_POST_NOT_FOUND)
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(instance=comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  ##TO DO 2 (create 구현)
  @swagger_auto_schema(
        operation_id='댓글 생성',
        operation_description='댓글을 생성합니다.',
        request_body= CommentListRequestSerializer,
        responses={200: CommentSerializer, 400: 'Bad Request', 403: 'Forbidden', 404: 'Not Found'}
  )
  def post(self, request):
    content = request.data.get("content")
    post = request.data.get("post")
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
    if not content:
      return Response(
          {"detail": "content fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    if not post:
      return Response({"detail": "post field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    
    try:
      post = Post.objects.get(id=post)
    except:
      return Response(
        {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
      )

    try:
        author = User.objects.get(username=username)
        if not author.check_password(password):
            return Response(
                {"detail": "Password is incorrect."},
                status=status.HTTP_403_BAD_REQUEST,
            )
        post = Comment.objects.create(content=content, post=post, author=author)
    except:
        return Response(
            {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
        )

