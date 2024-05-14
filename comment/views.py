from django.shortcuts import render
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from .serializers import CommentSerializer

# Create your views here.
class CommentListView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 목록 조회",
    operation_description="",
    responses={200: CommentSerializer, 404: "Not Found"},
  )
  def get(self, request):
    pass

  @swagger_auto_schema(
    operation_id="댓글 생성",
    operation_description="",
    request_body=CommentListRequestSerializer,
    responses={201: CommentSerializer, 400: "Bad Request", 403: "Forbidden", 404: "Not Found"},
  )
  def post(self, request):
    pass

class CommentDetailView(APIView):
  @swagger_auto_schema(
    operation_id="댓글 수정",
    operation_description="",
    request_body=CommentDetailRequestSerializer,
    responses={200: CommentSerializer, 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def put(self, request, comment_id):
    pass

  @swagger_auto_schema(
    operation_id="댓글 삭제",
    operation_description="",
    responses={204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found"},
  )
  def delete(self, request, comment_id):
    pass