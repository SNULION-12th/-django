from rest_framework.views import APIView
from post.models import Post
from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from .serializer import CommentSerializer
from .models import Comment
from account.models import User
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from drf_yasg import openapi
from account.request_serializers import SignInRequestSerializer

class CommentListView(APIView):

  postId = openapi.Parameter('post', openapi.IN_QUERY, description='post param', required=True, type=openapi.TYPE_INTEGER)

  @swagger_auto_schema(
      operation_id="게시글 댓글 목록 조회",
      operation_description="게시글 댓글 목록을 조회합니다.",
      responses={
            200: CommentSerializer(many=True),
            404: "Not Found",
      },
      manual_parameters=[postId]
      
  )
  def get(self, request):
    try:
      param = request.GET.get("post")
      post = Post.objects.get(id=param)
    except:
      return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    comments = Comment.objects.filter(post=post)
    comments_serializer = CommentSerializer(instance=comments, many=True)
    return Response(comments_serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
      operation_id="게시글 댓글 생성",
      operation_description="게시글 댓글을 생성합니다.",
      request_body=CommentListRequestSerializer,
      responses={200: CommentSerializer, 404: "Not Found", 403: "Forbidden", 400: "Bad Request"},
  )
  def post(self, request):
    postId = request.data.get("post")
    author_info = request.data.get("author")
    content = request.data.get("content")

    if not author_info:
      return Response(
        {"detail": "author field missing"}, status=status.HTTP_400_BAD_REQUEST
      )
    
    username = author_info.get("username")
    password = author_info.get("password")

    if not username or not password:
        return Response(
            {"detail": "[username, password] fields missing in author"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    if not postId:
      return Response(
        {"detail": "Post field missing"}, status=status.HTTP_400_BAD_REQUEST
      )

    if not content:
      return Response(
        {"detail": "Content field missing"}, status=status.HTTP_400_BAD_REQUEST
      )
    
    try:
      post = Post.objects.get(id=postId)
    except:
      return Response({"detail": "Post Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
      author = User.objects.get(username=username)
      
      if not author.check_password(password):
        return Response(
          {"detail": "Password is incorrect."},
            status=status.HTTP_403_FORBIDDEN,
        )
      comment = Comment.objects.create(post=post, content=content, author=author)
      

    except:
      return Response(
        {"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND
      )
    
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetailView(APIView):
  @swagger_auto_schema(
      operation_id="게시글 댓글 수정",
      operation_description="게시글 댓글을 수정합니다.",
      request_body=CommentDetailRequestSerializer,
      responses={200: CommentSerializer, 404: "Not Found", 401: "Unauthorized", 400: "Bad Request"},
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
      if not user.check_password(password):
        return Response({"detail": "Wrong Password"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
      comment = Comment.objects.get(id=commentId)
    except:
      return Response({"detail": "Comment Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if comment.author != user:
      return Response({"detail": "Unauthorized Comment"},status=status.HTTP_401_UNAUTHORIZED)
    
    comment.content = content
    comment.save()

    comment_serializer = CommentSerializer(instance=comment)
    
    return Response(comment_serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
      operation_id="게시글 댓글 삭제",
      operation_description="게시글 댓글을 삭제합니다.",
      request_body=SignInRequestSerializer,
      responses={
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        404: "Not Found"
      }
  )
  def delete(self, request, commentId):
    
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
      return Response({"detail": "[username, password] field missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      user = User.objects.get(username=username)
      if not user.check_password(password):
        return Response({"detail": "Wrong Password"}, status=status.HTTP_403_FORBIDDEN)
    except:
      return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
      comment = Comment.objects.get(id=commentId)
    except:
      return Response({"detail": "Comment Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    if comment.author != user:
      return Response({"detail": "Unauthorized Comment"}, status=status.HTTP_401_UNAUTHORIZED)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
