from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer, SignInRequestSerializer
from post.models import Post
from django.contrib.auth.models import User

from comment.serializers import CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentListView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 목록 조회",
        operation_description="특정 post의 모든 댓글을 조회합니다.",
        # 상언오빠가 도와준 쿼리 매개변수 추가...
        manual_parameters=[
            openapi.Parameter(
                'post',
                openapi.IN_QUERY,
                description="포스트 ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: CommentSerializer(many=True), 404: "Not Found"},
    )
  
    def get(self, request):
        # request의 post id를 받는다.
        post_id = request.GET.get("post")
        
        try:
          # request에서 전달받은 post_id를 가지고 우리 DB에 존재하는 Post 테이블을 서칭해서 같은 post id 찾기 
          Post.objects.get(id=post_id)
        except:
          return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # 특정 post의 모든 comment를 리턴한다.
        # 우리 DB에 존재하는 Comment 테이블에서 post_id로 필터링하겠다.
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="특정 Post에 댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
    )
    
    # 오민이 코드다.
    def post(self, request):
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "missing fields ['author']"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        post_id = request.data.get("post")
        content = request.data.get("content")
        
        if not username or not password:
            return Response(
                {"detail": "missing fields ['username', 'password']"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not post_id or not content:
            return Response(
                {"detail": "missing fields ['post', 'content']"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is wrong!"}, status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND
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
        operation_description="특정 댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
    )
    
    def put(self, request, comment_id):
      content = request.data.get('content')
      author_info = request.data.get("author")

      if not all([content, author_info]):
        return Response({"detail": "Missing fields in request."}, status=status.HTTP_400_BAD_REQUEST)

      username = author_info.get("username")
      password = author_info.get("password")

      if not all([username, password]):
        return Response(
          {"detail": "Missing field."},
          status=status.HTTP_400_BAD_REQUEST,
        )
      try:
          author = User.objects.get(username=username)
          if not author.check_password(password):
            return Response(
              {"detail": "Wrong password"}, status=status.HTTP_403_FORBIDDEN,
              )
            
      except User.DoesNotExist:
          return Response(
            {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )    
      try:
        comment = Comment.objects.get(id=comment_id)
      except Comment.DoesNotExist:
        return Response(
          {"detail": "No comment"}, status=status.HTTP_404_NOT_FOUND
          )  
      if comment.author != author:
        return Response(
          {"detail": "No authorization of comment."}, status=status.HTTP_403_FORBIDDEN,
          )

      comment.content = content
      comment.save()

      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="특정 댓글을 삭제합니다.",
    request_body=SignInRequestSerializer,
    responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},
)
    def delete(self, request, comment_id):
      username = request.data.get("username")
      password = request.data.get("password")
      if not all([username, password]):
        return Response({"detail": "Missing field in author info."}, status=status.HTTP_400_BAD_REQUEST)

      try:
        author = User.objects.get(username=username)
        if not author.check_password(password):
          return Response(
            {"detail": "Wrong Password or no authorization of comment"}, status=status.HTTP_403_FORBIDDEN,
            )
      except User.DoesNotExist:
        return Response(
          {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

      try:
        comment = Comment.objects.get(id=comment_id)
      except Comment.DoesNotExist:
        return Response(
          {"detail": "No comment"}, status=status.HTTP_404_NOT_FOUND
        )

      if comment.author != author:
        return Response(
          {"detail": "No permission to delete this comment."},
          status=status.HTTP_401_UNAUTHORIZED,
        )

      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    
    