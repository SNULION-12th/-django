from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from .request_serializers import CommentListRequestSerializer, CommentDetailRequestSerializer
from .serializers import CommentSerializer
from post.models import Post
from account.models import User
from .models import Comment

# Create your views here.
class CommentListView(APIView):
	@swagger_auto_schema(
		operation_id='댓글 목록 조회',
    operation_description='이 게시물의 댓글 목록을 조회합니다.',
		manual_parameters=[
			openapi.Parameter('post', openapi.IN_QUERY,
                             description="post_id",
                             type=openapi.TYPE_INTEGER)
    ],
  	responses={
      200: CommentSerializer(many=True),
      404: "Not Found",
    },
	)
	def get(self, request):
		#post id 잘못 되면 404
		post_id = request.GET.get('post')
		try:
			post = Post.objects.get(id=post_id)
			comments = post.comment.all() #comment 객체의 post 필드에서 foreign key로 연관관계 설정시 related_name으로 "comment"를 줘서 이렇게 접근 가능한거임! 
			#all() 주의!!
			if comments.count() > 0: #시리얼라이저에 빈거 못들어가서 따로 에러처리 해주기
				serializer = CommentSerializer(comments, many=True)
				return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				return Response({}, status=status.HTTP_200_OK)
		except:
			return Response({"detail" : "Wrong post id."}, status=status.HTTP_404_NOT_FOUND)
		

	@swagger_auto_schema(
		operation_id='댓글 생성',
    operation_description='게시물에 댓글을 생성합니다.',
		request_body=CommentListRequestSerializer,
  	responses={
      200: CommentSerializer(),
			400: "Bad Request",
			403: "Forbidden",
      404: "Not Found",
    },
	)
	def post(self, request):

		if not request.user.is_authenticated:
			return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
		author = request.user

		#아래는 인증/인가 처리 전 코드
		#author = request.data.get("author")

		post = request.data.get("post")
		content = request.data.get("content")
		if not post or not content:
			return Response({"detail" : "Missing field in request."}, status=status.HTTP_400_BAD_REQUEST)
		
		#아래는 인증/인가 처리 전 코드
		'''username = author.get("username") #author은 json이므로 그냥 막 필드 꺼내쓸 수 없음-> get 꼭 필요!
		password = author.get("password")
		try:
			author_user = User.objects.get(username = username)
			if not author_user.check_password(password):
				return Response(
					{"detail" : "Password is incorrect."},
					status = status.HTTP_403_FORBIDDEN,
				)
		except:
			return Response(
				{"detail" : "author not found."},
				status=status.HTTP_404_NOT_FOUND,
			)'''

		try:
			post_real = Post.objects.get(id = post)
		except:
			return Response(
				{"detail" : "Post not found."},
				status = status.HTTP_404_NOT_FOUND,
			)
		
		comment_to_save = Comment.objects.create(post = post_real, author = author, content = content) #인증/인가 처리 후 author_user에서 author로 수정
		#주의!! 객체 생성 혹은 조회시 받아온 request data를 그냥 넣으면 안되고, 무조건 db에서 찾아온 데이터로 넣어야함! 
		serializer = CommentSerializer(comment_to_save)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
	@swagger_auto_schema(
		operation_id='댓글 수정',
    operation_description='원하는 댓글을 수정합니다.',
		request_body=CommentDetailRequestSerializer,
		manual_parameters=[
			openapi.Parameter('comment_id', openapi.IN_PATH,
                             description="comment_id",
                             type=openapi.TYPE_STRING)	
    ],
  	responses={
      200: CommentSerializer(),
			400: "Bad Request",
			401: "Unauthorized",
      404: "Not Found",
    },
	)
	def put(self, request, comment_id):

		if not request.user.is_authenticated:
			return Response(
	                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
	            )				
		author = request.user

		#아래는 인증/인가 전 코드
		#author_data = request.data.get("author")

		content_data = request.data.get("content")
		if not content_data:
			return Response({"detail" : "Missing field in request."}, status=status.HTTP_400_BAD_REQUEST)
		
		#아래는 인증/인가 전 코드
		'''username_data = author_data.get("username")
		password_data = author_data.get("password")
		try:
			author = User.objects.get(username = username_data)
			if not author.check_password(password_data):
				return Response({"detail" : "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
		except:
			return Response({"detail" : "Author not found."}, status=status.HTTP_404_NOT_FOUND)'''
		
		try:
			comment = Comment.objects.get(id=comment_id)
			if comment.author != author:
				return Response({"detail" : "No authorization of comment."}, status=status.HTTP_403_FORBIDDEN)
		except:
			return Response({"detail" : "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
		
		#아래는 인증/인가 전 코드
		'''comment.author = author
		comment.content = content_data
		comment.save()
		serializer = CommentSerializer(comment)'''

		comment.content = content_data
		serializer = CommentSerializer(comment, data=request.data, partial=True)
		if not serializer.is_valid():
			return Response(
	                {"detail": "data validation error"}, status=status.HTTP_400_BAD_REQUEST
									)
		
		serializer.save()
		return Response(serializer.data,status=status.HTTP_200_OK)


	@swagger_auto_schema(
		operation_id='댓글 삭제',
    operation_description='원하는 댓글을 삭제합니다.',
		manual_parameters=[
			openapi.Parameter('comment_id', openapi.IN_PATH,
                             description="comment_id",
                             type=openapi.TYPE_STRING)	
    ],
		request_body=CommentDetailRequestSerializer,
  	responses={
      204: "No Content",
			400: "Bad Request",
			401: "Unauthorized",
      404: "Not Found",
    },
	)
	def delete(self, request, comment_id):

		if not request.user.is_authenticated:
			return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )

		#아래는 인증/인가 전 코드
		'''author_data = request.data.get("author")
		if not author_data:
			return Response({"detail" : "Missing field in request."}, status=status.HTTP_404_NOT_FOUND)
		
		username_data = author_data.get("username")
		password_data = author_data.get("password")
		try:
			author = User.objects.get(username = username_data)
			if not author.check_password(password_data):
				return Response({"detail" : "Password is incorrect."}, status=status.HTTP_403_FORBIDDEN)
		except:
			return Response({"detail" : "User not found."}, status=status.HTTP_404_NOT_FOUND)'''
		
		try:
			comment = Comment.objects.get(id=comment_id)
			if comment.author != author:
				return Response({"detail" : "No authorization of comment."}, status = status.HTTP_401_UNAUTHORIZED)
		except:
			return Response({"detail" : "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
		
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
