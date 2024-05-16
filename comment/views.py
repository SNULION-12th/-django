from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Comment,User
from .serializers import CommentSerializer
from .request_serializers import CommentCreateRequestSerializer, CommentDeleteRequestSerializer, CommentListRequestSerializer, CommentUpdateRequestSerializer
from drf_yasg.utils import swagger_auto_schema

from account.models import User
from account.request_serializers import SignInRequestSerializer

class PostCommentView(APIView):
    @swagger_auto_schema(
        operation_id="create_comment",
        operation_description="새 댓글을 생성합니다.",
        request_body=CommentCreateRequestSerializer,
        responses={201: CommentSerializer, 400: "Missing Field in Request", 403: "Wrong Password", 404: "Author or Post not Found"},
    )
    def post(self, request):
        requestBody = CommentCreateRequestSerializer(data=request.data)
        signin_serializer = SignInRequestSerializer(data=requestBody.author)
        try:
          result = signIn(signin_serializer.username,signin_serializer.password) ##정상실행되면 auth정보가 담겨있음
          if result is 1:
            return Response("Password Not Match", status=status.HTTP_403_FORBIDDEN)
          elif result is 2:
            return Response("Author or Post not found", status=status.HTTP_404_NOT_FOUND)
          newComment = Comment.objects.create(post = requestBody.post, author = result, content = requestBody.content)
          return Response(CommentSerializer(newComment).data,status=status.HTTP_201_CREATED)
        except:
          return Response("Internal Server Error",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    @swagger_auto_schema(
        operation_id="show_comment_list",
        operation_description="한 Post에 대한 Comment List를 반환합니다.",
        request_body=CommentListRequestSerializer,
        responses={200: Comment, 400: "Bad Request"},
    )
    def get(self, request):
        target_post_serializer = CommentListRequestSerializer(data=request.data)
        if target_post_serializer.is_valid(raise_exception=True):
          return Response(Comment.objects.get(), status=status.HTTP_200_OK) #####여기 수정해야됨 List로######
        return Response("Post not found.",status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
      @swagger_auto_schema(
        operation_id="회원가입",
        operation_description="회원가입을 진행합니다.",
        request_body=SignUpRequestSerializer,
        responses={201: UserProfileSerializer, 400: "Bad Request"},
    )
      def put(self, request):

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user.password)
            user.save()

        college = request.data.get("college")
        major = request.data.get("major")

        user_profile = UserProfile.objects.create(
            user=user, college=college, major=major
        )
        user_profile_serializer = UserProfileSerializer(instance=user_profile)
        return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
      
      @swagger_auto_schema(
        operation_id="회원가입",
        operation_description="회원가입을 진행합니다.",
        request_body=SignUpRequestSerializer,
        responses={201: UserProfileSerializer, 400: "Bad Request"},
    )
      def delete(self, request):

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user.password)
            user.save()

        college = request.data.get("college")
        major = request.data.get("major")

        user_profile = UserProfile.objects.create(
            user=user, college=college, major=major
        )
        user_profile_serializer = UserProfileSerializer(instance=user_profile)
        return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)

# Create your views here.

def signIn(user_name, password):
        try:
            auth = User.objects.get(username=user_name)
            if not auth.check_password(password):
                return 1 ##password not match
            return auth
        except:
            return 2 ##user not found