from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, User

from .models import Comment
from .serializers import CommentSerializer


# Create your views here.
class CommentListView(APIView):
    def get(self, request):
        post_id = request.GET.get('post')
        if not post_id:
            return Response({"detail": "missing fields ['post']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        author = User.objects.get(username=request.data.get('username'))
        post_id = request.data.get('post')
        content = request.data.get('content')
        
        if not author:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        if author.password != request.data.get('password'):
            return Response({"detail": "Password is wrong!"}, status=status.HTTP_401_UNAUTHORIZED)
          

        if not post_id or not content:
            return Response({"detail": "missing fields ['post', 'content']"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Post.objects.filter(id=post_id).exists():
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        comment = Comment.objects.create(post_id=post_id, author=author, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentDetailView(APIView):
    def patch(self, request, comment_id):
        content = request.data.get('content')
        author = User.objects.get(username=request.data.get('username'))
        
        if not author:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        if author.password != request.data.get('password'):
            return Response({"detail": "Password is wrong!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not content:
            return Response({"detail": "missing fields ['content']"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        
        author = User.objects.get(username=request.data.get('username'))
        
        if not author:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if author.password != request.data.get('password'):
            return Response({"detail": "Password is wrong!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if author != comment.author:
            return Response({"detail": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        