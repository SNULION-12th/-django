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
from account.request_serializers import SignInRequestSerializer
##swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
class CommentListView(APIView): ##get, create
  #TO DO 1 (get 구현)
  @swagger_auto_schema(
        operation_id='댓글 목록 조회',
        operation_description='게시물의 댓글 목록을 조회합니다.',
        manual_parameters=[
          openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="post",
            type=openapi.TYPE_INTEGER,
            required=True
          ),
        ],
        responses={200: CommentSerializer(many=True), 404: 'Not Found'}
  )
  def get(self, request):
    post_id = request.GET.get("post")
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
    author = request.user
    if not request.user.is_authenticated:
        return Response(
            {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
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
    except:
        return Response(
            {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
        )
    comment = Comment.objects.create(content=content, post=post, author=author)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailView(APIView):
  @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 403:'Unauthorized', 404: "Not Found", 400: "Bad Request"},
    )
  def put(self, request, comment_id):
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response(
        {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    author = request.user
    if not request.user.is_authenticated:
        return Response(
            {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
        )
        
    if comment.author != author:
          return Response(
            {'detail': 'No Authorization of comment'}, status=status.HTTP_403_FORBIDDEN
          )
    
    content = request.data.get("content")
    if not content:
      return Response(
          {"detail": "content fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    ## 오류처리 끝, 수정 기능 구현 시작
    comment.content = content
    comment.save()
    serializer = CommentSerializer(instance=comment)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @swagger_auto_schema(
        operation_id="댓글 삭제",
        operation_description="댓글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: 'No Content', 400: "Bad Request", 403:'Unauthorized', 404: "Not Found"},
    )
  def delete(self, request, comment_id):
    try:
      comment = Comment.objects.get(id=comment_id)
    except:
      return Response(
        {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
      )
    
    author = request.user
    if not request.user.is_authenticated:
        return Response(
            {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
        )
    if comment.author != author:
      return Response(
        {'detail': 'No Authorization of comment'}, status=status.HTTP_403_FORBIDDEN
      )
    
    content = request.data.get("content")
    if not content:
      return Response(
          {"detail": "content fields missing."},
          status=status.HTTP_400_BAD_REQUEST,
      )
    
    comment.delete()
    return Response(
      status=status.HTTP_204_NO_CONTENT
    )