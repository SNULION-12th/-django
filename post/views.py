from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post, Like
from drf_yasg.utils import swagger_auto_schema
from .request_serializers import PostListRequestSerializer, PostDetailRequestSerializer
from account.models import User
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer

# Create your views here.
class PostListView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 목록 조회',
            operation_description='게시글 목록을 조회합니다.',
            responses={
            200: PostSerializer(many=True),
            404: "Not Found",
            400: "Bad Request",
            },
        )
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) #직렬화할 데이터가 많으므로 many=True 넣어주기
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_id="게시글 생성",
        operation_description="게시글을 생성합니다.",
        request_body=PostListRequestSerializer,
        responses={201: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request): #이 api가 좀 갈아엎어짐 
        title = request.data.get("title") #요청으로부터 제목, 내용, 태그, 작성자 정보 뽑아오기
        content = request.data.get("content")
        tag_contents = request.data.get("tags")
        author_info = request.data.get("author")
        if not author_info: #작성자 없다면 빠졌다고 에러 리턴
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username") #작성자 객체로부터 작성자의 유저네임과 비번 정보 뽑아오기
        password = author_info.get("password")
        if not username or not password: #둘 중에 하나라도 없다면 에러 리턴
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not title or not content: #제목과 내용 중에 하나라도 없다면 에러 리턴
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username) #유저 db에서 유저네임(primary key)와 일치하는 유저 객체를 뽑아오기(작성자임)
            if not author.check_password(password): #기존에 저장된 비밀번호와 요청에서 뽑아온 작성자 정보의 비밀번호(현재 로그인한 사람의 비번)이 같지 않으면 에러 리턴
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post = Post.objects.create(title=title, content=content, author=author) #받아온 제목, 내용 작성자 정보로 게시물 객체를 만들어서 저장
        except: #해당 유저네임과 일치하는 유저 객체 자체가 없었을 경우에는 에러 리턴
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if tag_contents is not None: #요청에 태그가 있을 경우에만 아래 내용 실행
            for tag_content in tag_contents: #태그 내의 각 태그에 대해
                if not Tag.objects.filter(content=tag_content).exists(): #태그 db 내에 없던 태그라면
                    post.tags.create(content=tag_content) #태그를 생성해서 저장함
                else:
                    post.tags.add(Tag.objects.get(content=tag_content)) #그렇지 않다면 이 태그 객체를 찾아서 post.tags에 새롭게 매핑

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            responses={200: PostSerializer, 400: "Bad Request"}
        )
    def get(self, request, post_id): #url에서 id 변수 받아와서 쓸거라고 명시
        try: #게시물을 찾을 수 있는지 분기처리
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id="게시글 삭제",
        operation_description="게시글을 삭제합니다.",
        request_body=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request"},
    )
    def delete(self, request, post_id):
        try: #삭제 대상이 되는 게시물 아이디를 바탕으로 개시물 객체를 찾음 -> 못찾으면 에러 리턴
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        author_info = request.data #요청의 데이터는 작성자의 데이터와 같음(SignInRequestSerializer이 요청 처리의 역할을 함)
        if not author_info: #작성자 데이터가 없다면 에러 처리
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username") #작성자 데이터로부터 유저네임과 비밀번호를 뽑아냄
        password = author_info.get("password")
        if not username or not password: # 둘 중에 하나라도 없다면 에러리턴
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username) #작성자의 유저네임과 일치하는 유저 객체를 뽑아서 작성자로 생각
            if not author.check_password(password): #db에 저장된 작성자의 비번과 현재 로그인한 유저의 비번이 다르다면 에러 리턴
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if post.author != author: #삭제 대상이 되는 게시물의 작성자와 삭제 요청을 보낸 유저가 다르다면 에러 리턴 
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except: #애초에 유저 db에서 요청 받은 작성자 정보에 해당하는 유저 객체 자체가 없었으면 에러 리턴
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_id="게시글 수정",
        operation_description="게시글을 수정합니다.",
        request_body=PostDetailRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def put(self, request, post_id): #위의 두 api의 혼합이므로 알아서 이해
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

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
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.title = title
        post.content = content

        tag_contents = request.data.get("tags")
        if tag_contents is not None:
            post.tags.clear()
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        post.save()
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LikeView(APIView):
    @swagger_auto_schema(
        operation_id="좋아요 토글",
        operation_description="좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.",
        request_body=SignInRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request, post_id):

        ### 1 ### 좋아요를 누를 게시글을 특정하는 부분. post_id를 id 값으로 가지는 Post 객체가 있다면 그 객체를 post에 할당하고 만약 없다면 에러 리턴
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ### 2 ### 유저를 특정하는 부분
        # request의 body 로 전달된 username을  값으로 가지는 User 객체가 있다면 그 객체를 user에 할당하고 만약 없다면 에러 리턴
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        ### 3 ### 게시물의 좋아요 중 현재 유저가 남긴 것이 있는지 체크
        is_liked = post.like_set.filter(user=author).count() > 0 #like_set에는 유저들의 queryset 객체가 담겨있음

        ### 4 ### 좋아요를 누른적이 있다면 취소하고, 누른적이 없다면 눌러줌
        if is_liked == True:
            post.like_set.get(user=author).delete()
            print("좋아요 취소")
        else:
            Like.objects.create(user=author, post=post) #좋아요 db에 해당 유저와 게시글 저장
            print("좋아요 누름")

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)