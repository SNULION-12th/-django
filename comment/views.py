from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment,User
from .serializers import CommentSerializer
from .request_serializers import CommentCreateRequestSerializer, CommentDeleteRequestSerializer, CommentListRequestSerializer, CommentUpdateRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.models import User
from account.request_serializers import SignInRequestSerializer

class PostCommentView(APIView):
    @swagger_auto_schema(
        operation_id="create_comment",
        operation_description="새 댓글을 생성합니다.",
        request_body=CommentCreateRequestSerializer(many = False),
        responses={201: CommentSerializer, 400: "Missing Field in Request", 403: "Wrong Password", 404: "Author or Post not Found"},
    )
    def post(self, request):
        requestBody = CommentCreateRequestSerializer(data=request.data)
        signin_serializer = SignInRequestSerializer(data=requestBody.author)
        try:
          result = signIn(signin_serializer.username,signin_serializer.password) ##정상실행되면 auth정보가 담겨있음
          if result == 1:
            return Response("Password Not Match", status=status.HTTP_403_FORBIDDEN)
          elif result == 2:
            return Response("Author or Post not found", status=status.HTTP_404_NOT_FOUND)
          newComment = Comment.objects.create(post = requestBody.post, author = result, content = requestBody.content)
          return Response(CommentSerializer(newComment).data,status=status.HTTP_201_CREATED)
        except:
          return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    @swagger_auto_schema(
      operation_id="get_all_comment_per_post",
      operation_description="특정 Post에 대한 모든 Comment를 반환합니다.",
      query_serializer=CommentListRequestSerializer,
      responses={200: CommentSerializer(many=True), 404: "Not Found"}
    )
    def get(self, request):
        target_post_serializer = CommentListRequestSerializer(data=request.data)
        if target_post_serializer.is_valid(raise_exception=True):
          comments = Comment.objects.get(post = target_post_serializer.post)
          commentSerializer = CommentSerializer(comments, many = True)
          return Response(commentSerializer.data, status=status.HTTP_200_OK)
        return Response("Post not found.",status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
      @swagger_auto_schema(
        operation_id="update_comment",
        operation_description="댓글을 수정합니다.",
        request_body=CommentUpdateRequestSerializer(many = False),
        responses={200: CommentSerializer, 400: "Missing Field", 403: "Authorization Failure", 404: "Author or Comment Not Found"},
    )
      def put(self, request):
        try:
          requestBody = CommentUpdateRequestSerializer(data=request.data)
          signin_serializer = SignInRequestSerializer(data=requestBody.author)
          content_serializer = CommentCreateRequestSerializer(data=requestBody.data)
          result = signIn(signin_serializer.username,signin_serializer.password) ##정상실행되면 auth정보가 담겨있음
          if result == 1:
            return Response("Authorization Failure", status=status.HTTP_403_FORBIDDEN)
          elif result == 2:
            return Response("Author or Comment not found", status=status.HTTP_404_NOT_FOUND)
          newComment = Comment.objects.get(post = requestBody.post)
          newComment.content = content_serializer.content
          newComment.save()
          return Response(CommentSerializer(newComment).data,status=status.HTTP_200_OK)
        except:
          return Response("Missing Field",status=status.HTTP_400_BAD_REQUEST)
      
      @swagger_auto_schema(
        operation_id="delete_comment",
        operation_description="Comment를 삭제합니다.",
        request_body=CommentDeleteRequestSerializer(many = False),
        responses={204: "No Content", 403: "Authorization Failure", 404: "Missing Field or Comment Not Found"},
    )
      def delete(self, request):
          requestBody = CommentDeleteRequestSerializer(data=request.data)
          signin_serializer = SignInRequestSerializer(data=requestBody.author)
          result = signIn(signin_serializer.username,signin_serializer.password) ##정상실행되면 auth정보가 담겨있음
          if result == 1:
            return Response("Authorization Failure", status=status.HTTP_403_FORBIDDEN)
          elif result == 2:
            return Response("Missing Field or Comment Not Found", status=status.HTTP_404_NOT_FOUND)
          targetComment = Comment.get(id = requestBody.comment_id)
          targetComment.delete()
          return Response("No Content",status=status.HTTP_204_NO_CONTENT)

# Create your views here.

def signIn(user_name, password):
        try:
            auth = User.objects.get(username=user_name)
            if not auth.check_password(password):
                return 1 ##password not match
            return auth
        except:
            return 2 ##user not found