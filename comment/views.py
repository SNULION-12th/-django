from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from account.models import User
from post.models import Post
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentListView(APIView):
    
    @swagger_auto_schema(
        operation_id="댓글 조회",
        operation_description="댓글을 조회합니다.",
        manual_parameters=[
        openapi.Parameter(
            'post',
            openapi.IN_QUERY,
            description="post id",
            type=openapi.TYPE_INTEGER
        ),
    ],
        responses={200: CommentSerializer, 404: "Not Found"},)
    
    def get(self, request,):
        postId= request.GET.get('post')
        try:
            Post.objects.get(id=postId)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
		
        comments = Comment.objects.filter(post_id=postId)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_id="댓글 생성",
        operation_description="댓글을 생성합니다.",
        request_body=CommentListRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},)
    
    def post(self, request ):
        content = request.data.get("content")
        post_info = request.data.get("post")
        author_info = request.data.get("author")
        if not author_info :
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not post_info :
            return Response(
                {"detail": "post field missing."}, status=status.HTTP_400_BAD_REQUEST
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
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                {"detail": "Password is incorrect."},
                status=status.HTTP_403_Forbidden,
                )
        except:
            return Response(
                {"detail": " Not found."}, status=status.HTTP_404_NOT_FOUND
            )
            
        try:
            post = Post.objects.get(id=post_info)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comment = Comment.objects.create(post_id =  post_info, content=content, author=author)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )


        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    @swagger_auto_schema(
        operation_id="댓글 수정",
        operation_description="댓글을 수정합니다.",
        request_body=CommentDetailRequestSerializer,
        responses={200:CommentSerializer , 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},)
    
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND)
				
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if comment.author != author:
                return Response(
                    {"detail": "You are not the author of this comment."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get("content")
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
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found"},)
    
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
                status=status.HTTP_403_Forbidden,
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
    