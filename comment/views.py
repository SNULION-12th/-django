from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from account.request_serializers import SignInRequestSerializer
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from post.models import Post
from drf_yasg.utils import swagger_auto_schema
from account.models import User
from drf_yasg import openapi


# class CommentListView(APIView):
#     def get(self, request):
#         try: 
#             post_id = request.GET.get('post')
#             Post.objects.get(id = post_id)
#             comments = Comment.objects.filter(post=post_id)
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except:
#             return Response({"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request):
#         author_info = request.data.get("author")
#         post_id = request.data.get("post")
#         content = request.data.get("content")
#         if not author_info: 
#             return Response(
#                  {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
#                  )
#         username = author_info.get("username")
#         password = author_info.get("password")
#         if not username or not password:
#             return Response(
#                  {"detail": "[username, password] fields missing in author"},
#                  status=status.HTTP_400_BAD_REQUEST,
#              )
#         if not post_id or not content:
#             return Response(
#                  {"detail": "[content] fields missing."},
#                  status=status.HTTP_400_BAD_REQUEST,
#              )
#         try:
#             author = User.objects.get(username=username)
#             if not author.check_password(password):
#                 return Response(
#                     {"detail": "Password is incorrect."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             comment = Comment.objects.create(post_id=post_id, content=content, author=author)
#         except:
#             return Response(
#                 {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = CommentSerializer
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
  
# class CommentDetailView(APIView):
#     def put(self, request, comment_id):
#         try:
#             comment = Comment.objects.get(id=comment_id)
#         except:
#             return Response(
#                 {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         author_info = request.data.get("author")
#         if not author_info:
#             return Response(
#                 {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
#             )
#         username = author_info.get("username")
#         password = author_info.get("password")
#         if not username or not password:
#             return Response(
#                  {"detail": "[username, password] fields missing in author"},
#                  status=status.HTTP_400_BAD_REQUEST,
#              )
#         try:
#             author = User.objects.get(username=username)
#             if not author.check_password(password):
#                 return Response(
#                     {"detail": "Password is incorrect."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if comment.author != author:
#                 return Response(
#                     {"detail": "You are not the author of this post."},
#                     status=status.HTTP_403_FORBIDDEN,
#                 )
#         except:
#             return Response(
#                 {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
#             )
        
#         content = request.data.get("content")
#         if not content:
#             return Response(
#                 {"deatail": "content fields missing."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         comment.content = content
#         comment.save()
#         serializer = CommentSerializer(instanace=comment)
#         return Response(serializer.data, status=status.HTTP_200_OK)
         
#     def delete(self, request, comment_id):
#         try:
#             comment = Comment.objects.get(id=comment_id)
#         except:
#             return Response(
#                 {"detail": "Comment Not found."}, status=status.HTTP_404_NOT_FOUND
#             )
#         author_info = request.data
#         if not author_info:
#             return Response(
#                 {"detail": "author field missing."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         username = author_info.get("username")
#         password = author_info.get("password")
#         try:
#             author = User.objects.get(username=username)
#             if not author.check_password(password):
#                 return Response(
#                     {"detail": "Password is incorrect."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if comment.author != author:
#                 return Response(
#                     {"detail": "You are not the author of this post."},
#                     status=status.HTTP_403_FORBIDDEN,
#                 )
#         except: 
#             return Response(
#                 {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
#             )
        
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
                
