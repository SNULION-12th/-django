from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer

from post.models import Post
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .request_serializers import CommentDetailRequestSerializer, CommentListRequestSerializer
from account.request_serializers import SignInRequestSerializer

# Create your views here.
class CommentListView(APIView):
    @swagger_auto_schema(
      operation_id='전체 댓글 조회',
      operation_description='전체 댓글을 조회합니다.',
      manual_parameters=[
        openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="post id",
            type=openapi.TYPE_INTEGER
        ),
    ],
      responses={200: CommentSerializer(many=True), 404: "Not Found"}
    )
    def get(self, request):
      post_id = request.GET.get('post')
      try:
          Post.objects.get(id=post_id)
      except:
          return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
      
      comments = Comment.objects.filter(post_id=post_id)
      serializer = CommentSerializer(instance=comments, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
      operation_id='댓글 생성',
      operation_description='댓글을 생성합니다.',
      request_body=CommentListRequestSerializer,
      responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"}
    )

    def post(self, request):
      content = request.data.get('content')
      author_info = request.data.get("author")
      post_id = request.data.get('post')

      if not all([content, post_id, author_info]):
          return Response({"detail": "Missing fields in request."}, status=status.HTTP_400_BAD_REQUEST)    

      username = author_info.get("username")
      password = author_info.get("password")
  
      if not all([username, password]):
            return Response({"detail": "Missing fields in author info."}, status=status.HTTP_400_BAD_REQUEST)
      
      try:
          author = User.objects.get(username=username)
          if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
          
      except User.DoesNotExist:
          return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
  
      try:
            post = Post.objects.get(id=post_id)
      except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

      comment = Comment.objects.create(content=content, author=author, post=post)
      serializer = CommentSerializer(instance = comment)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
 
class CommentDetailView(APIView):

    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="특정 댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
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
            {"detail": "Missing fields in author info."},
            status=status.HTTP_400_BAD_REQUEST,
        )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
              return Response(
               {"detail": "Password is incorrect."},
                status=status.HTTP_403_FORBIDDEN,
              )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )    
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )  
        if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
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
            return Response({"detail": "Missing fields in author info."}, status=status.HTTP_400_BAD_REQUEST)

      try:
          author = User.objects.get(username=username)
          if not author.check_password(password):
            return Response(
              {"detail": "Password is incorrect."},
              status=status.HTTP_403_FORBIDDEN,
              )
      except User.DoesNotExist:
          return Response(
            {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

      try:
        comment = Comment.objects.get(id=comment_id)
      except Comment.DoesNotExist:
        return Response(
            {"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
        )

      if comment.author != author:
        return Response(
            {"detail": "You do not have permission to delete this comment."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

      comment.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)