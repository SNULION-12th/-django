from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import commentSerializer
from drf_yasg.utils import swagger_auto_schema
from post.models import Post
from account.models import User
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from account.request_serializers import SignInRequestSerializer
from drf_yasg import openapi

class CommentListView(APIView):
  @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="게시글의 댓글을 조회합니다.",
        manual_parameters=[
        openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="post id",
            type=openapi.TYPE_INTEGER
        ),
    ],
        responses={
            200: commentSerializer(many=True),
            404: "Not Found",
        },
    )
  def get(self, request):
    post_id = request.GET.get("post", None)
    if not Comment.objects.filter(post=post_id).exists():
      return Response({"detail": "post not found"}, status = status.HTTP_404_NOT_FOUND)
    comments = Comment.objects.filter(post=post_id)
    serializer = commentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={
          201: commentSerializer,
          404: "Not Found", 
          403: "Forbidden",
          400: "Bad Request",
        },
  )
  def post(self, request):
    author_info = request.data.get("author")
    post_id = request.data.get("post")
    content = request.data.get("content")
    #- check if author_info is empty
    if not author_info:
      return Response(
          {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get("username")
    password = author_info.get("password")

    #- check if username & pw is empty
    if not username or not password:
      return Response(
          {"detail": "[username, password] fields missing in author"},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    #- check if post_id or content is empty
    if not post_id or not content:
      return Response(
          {"detail": "[post_id, content] fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    try:
      #- finding actual user object
      author = User.objects.get(username=username)
      #- check if password is incorect
      if not author.check_password(password):
        return Response(
          {"detail": "Password is incorrect."},
          status=status.HTTP_403_FORBIDDEN,
        )
    except:
      return Response(
        {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    newComment = Comment.objects.create(post_id=post_id, content=content, author=author)
    
    serializer = commentSerializer(newComment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
  @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댯글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: commentSerializer, 404: "Not Found", 400: "Bad Request", 401:"Unauthorized",},
    ) 
  def put(self, request, comment_id):
    author_info = request.data.get("author")
    content = request.data.get("content")
    if not author_info:
      return Response(
          {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get("username")
    password = author_info.get("password")

    #- check if username & pw is empty
    if not username or not password:
      return Response(
          {"detail": "[username, password] fields missing in author"},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    #- check if content is empty
    if not content:
      return Response(
          {"detail": "[content] fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    try:
      #- finding actual user object
      author = User.objects.get(username=username)
      #- check if password is incorect
      if not author.check_password(password):
        return Response(
          {"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN,
        )
    except:
      return Response(
        {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response({"detail":"Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    comment.content = content
    comment.save()
    serializer = commentSerializer(instance=comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request", 401: "Unauthorized"},
    )
  def delete(self, request, comment_id):
    author_info = request.data.get("author")
    if not author_info:
      return Response(
          {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get("username")
    password = author_info.get("password")

    #- check if username & pw is empty
    if not username or not password:
      return Response(
          {"detail": "[username, password] fields missing in author"},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    try:
      #- finding actual user object
      author = User.objects.get(username=username)
      #- check if password is incorect
      if not author.check_password(password):
        return Response(
          {"detail": "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN,
        )
    except:
      return Response(
        {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
      )
  
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response({"detail":"Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

