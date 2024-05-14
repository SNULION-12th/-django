from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from .serializers import CommentSerializer
from .models import Comment
from account.models import User
from post.models import Post
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
            description="post id",
            type=openapi.TYPE_INTEGER
        ),
    ],
    responses={200: CommentSerializer(many=True), 404: "Not Found"},
  )
  def get(self, request):
    post_id= request.GET.get('post')
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"detail": "No such post."}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(post_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    operation_id="댓글 생성",
    operation_description="댓글을 생성합니다.",
    request_body=CommentListRequestSerializer,
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
  )
  def post(self, request):
    author_info = request.data.get("author")
    post_id = request.data.get("post")
    content = request.data.get("content")

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
    
    if post_id is None:
       return Response(
          {"detail": "post field missing."}, status=status.HTTP_400_BAD_REQUEST
       )
    if not content:
       return Response(
          {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
       )
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"detail": "No such post."}, status=status.HTTP_404_NOT_FOUND)

    try:
        author = User.objects.get(username=username)
        if not author.check_password(password):
            return Response(
                {"detail": "Password is incorrect."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment = Comment.objects.create(content=content, post_id=post_id, author=author)
    except:
        return Response(
            {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 수정",
    operation_description="댓글을 수정합니다.",
    request_body=CommentDetailRequestSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def put(self, request, comment_id):
    author_info = request.data.get("author")
    content = request.data.get("content")

    if not author_info:
       return Response(
          {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
       )
    if not content:
       return Response(
          {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
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
       comment = Comment.objects.get(id=comment_id)
    except:
       return Response(
          {"detail": "No such comment"}, status=status.HTTP_404_NOT_FOUND
       )
    
    if comment.author != author:
      return Response(
        {"detail": "No authorization"}, status=status.HTTP_401_UNAUTHORIZED
      )

    comment.content = content
    comment.save()
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


  @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="댓글을 삭제합니다.",
    request_body=SignInRequestSerializer,
    responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def delete(self, request, comment_id):
    username = request.data.get("username")
    password = request.data.get("password")
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
       comment = Comment.objects.get(id=comment_id)
    except:
       return Response(
          {"detail": "No such comment"}, status=status.HTTP_404_NOT_FOUND
       )
    
    if comment.author != author:
      return Response(
        {"detail": "No authorization"}, status=status.HTTP_401_UNAUTHORIZED
      )
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
