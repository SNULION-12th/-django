from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from drf_yasg.utils import swagger_auto_schema

class PostListView(APIView):
		### 얘네가 class inner function 들! ###
    @swagger_auto_schema(
              operation_id='게시글 목록 조회',
              operation_description='게시글 목록을 조회합니다.',
              responses={200: PostSerializer(many=True)}
          )
    def get(self, request): 
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # contents = [{"id":post.id,
        #              "title":post.title,
        #              "content":post.content,
        #              "created_at":post.created_at
        #              } for post in posts]
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
            operation_id='게시글 생성',
            operation_description='게시글을 생성합니다.',
            request_body=PostSerializer,
            responses={201: PostSerializer}
        )
    
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):
    @swagger_auto_schema(
            operation_id='게시글 상세 조회',
            operation_description='게시글 1개의 상세 정보를 조회합니다.',
            responses={200: PostSerializer}
        )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
            operation_id='게시글 삭제',
            operation_description='게시글을 삭제합니다.',
            responses={204: 'No Content', 404: 'Not Found'}
        )    
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
                operation_id='게시글 수정',
                operation_description='게시글을 수정합니다.',
                responses={201: '수정 성공', 404: '수정 실패'}
            )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        post.title = request.data['title']
        post.content = request.data['content']
        post.save()

        return Response(status=status.HTTP_200_OK)
    
    

# 게시글 수정 메서드 추가: PostDetailView 클래스에 put 메서드를 추가합니다. 이 메서드는 게시글의 ID를 URL에서 받고, 요청의 본문에서 수정하고자 하는 제목과 내용을 추출합니다.
# 게시글 찾기: put 메서드 안에서, 주어진 post_id를 사용하여 데이터베이스에서 해당 게시글을 찾습니다. 만약 게시글이 존재하지 않는 경우, 적절한 에러 메시지와 함께 404 상태 코드를 반환합니다.
# 데이터 검증: 제목과 내용이 요청에 포함되어 있는지 확인합니다. 필수 필드가 누락되었다면, 필드가 누락되었다는 메시지와 400 상태 코드를 반환합니다.
# 게시글 수정: 게시글 객체의 제목과 내용을 요청 데이터로 업데이트하고, 데이터베이스에 저장합니다.
# 응답 반환: 수정된 게시글을 직렬화하여 클라이언트에게 JSON 형식으로 반환합니다. 상태 코드는 200(OK)를 사용합니다.
# Swagger 문서화: swagger_auto_schema 데코레이터를 사용하여 API 문서화에 필요한 정보를 추가합니다. 이는 수정 API의 명세를 자동으로 생성할 때 사용됩니다. 