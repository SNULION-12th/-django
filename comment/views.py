from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment
from .serializers import commentSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Post

class CommentListView(APIView):
  def get(self, request):
    postid = request.GET.get(postId)



class CommentDetailView(APIView):
