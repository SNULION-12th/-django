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

class CommentListView(APIView):
  def get(self, request):
    post_id = request.GET.get("post")
    if not Comment.objects.filter(post=post_id).exists():
      return Response({"detail": "post not found"}, status = status.HTTP_404_NOT_FOUND)
    comments = Comment.objects.filter(post=post_id)
    serializer = commentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
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
    
    if not post_id or not content:
      return Response(
          {"detail": "[post_id, content] fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    try:
      author = User.objects.get(username=username)
    except:
      return Response(
        {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    newComment = Comment.objects.create(post_id=post_id, content=content, author=author)
    
    serializer = commentSerializer(newComment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#class CommentDetailView(APIView):
#  def put(self, request, comment_id):
