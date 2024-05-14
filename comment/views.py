from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from post.models import Post
from .serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, CommentDeleteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from account.models import User
from .models import Comment

# Create your views here.

class CommentView(APIView):
  @swagger_auto_schema(
    operation_id="게시글의 댓글 전체 조회",
    operation_description="게시글 1개의 댓글들을 조회합니다.",
    responses={200: CommentSerializer, 400: "Bad request", 404: "Not Found"},
    manual_parameters=[
      openapi.Parameter(
        'post',
        openapi.IN_QUERY,
        description="게시글 ID",
        type=openapi.TYPE_INTEGER,
        required=True
      )
    ]
  )
  def get(self, request):
    post_id = request.GET.get('post', '')
    if post_id == '':
      return Response(
        {"detail": "post_id field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    try:
      post = Post.objects.get(id=post_id)
    except:
      return Response(
        {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND
      )
    comments = post.comment_list.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
    operation_id="게시글 댓글 작성",
    operation_description="게시글에 댓글을 생성합니다.",
    request_body=CommentCreateSerializer,
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
  )
  def post(self, request):
    author_info = request.data.get('author')
    post_id = request.data.get('post')
    content = request.data.get('content')

    if not author_info:
      return Response(
        {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get('username')
    password = author_info.get('password')
    if not username or not password:
      return Response(
        {"detail": "[username, password] fields missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    if not post_id or not content:
      return Response(
        {"detail": "[post, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response(
          {"detail": "Password wrong."}, status=status.HTTP_403_FORBIDDEN
        )
    except:
      return Response(
        {"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND
      )

    try:
      post = Post.objects.get(id=post_id)
    except:
      return Response(
        {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    comment = Comment.objects.create(post=post, content=content, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class CommentDetailView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 수정",
    operation_description="댓글을 수정합니다.",
    request_body=CommentUpdateSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def put(self, request, comment_id):
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response(
        {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    author_info = request.data.get('author')
    if not author_info:
      return Response(
        {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get('username')
    password = author_info.get('password')
    if not username or not password:
      return Response(
        {"detail": "[username, password] fields missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response(
          {"detail": "Password wrong."}, status=status.HTTP_400_BAD_REQUEST
        )
      if author != comment.author:
        return Response(
          {"detail": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED
        )
    except:
      return Response(
        {"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    content = request.data.get('content')
    if not content:
      return Response(
        {"detail": "content field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    
    comment.content = content
    comment.save()
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="댓글을 삭제합니다.",
    request_body=CommentDeleteSerializer,
    responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def delete(self, request, comment_id):
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response(
        {"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    author_info = request.data.get('author')
    if not author_info:
      return Response(
        {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    username = author_info.get('username')
    password = author_info.get('password')
    if not username or not password:
      return Response(
        {"detail": "[username, password] fields missing."}, status=status.HTTP_400_BAD_REQUEST
      )
    try:
      author = User.objects.get(username=username)
      if not author.check_password(password):
        return Response(
          {"detail": "Password wrong."}, status=status.HTTP_400_BAD_REQUEST
        )
      if author != comment.author:
        return Response(
          {"detail": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED
        )
    except:
      return Response(
        {"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND
      )

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)