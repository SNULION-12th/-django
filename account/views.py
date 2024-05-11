from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.request_serializers import SignInRequestSerializer, SignUpRequestSerializer

from .serializers import ( #필요한 serializer들을 받아오기 
    UserSerializer,
    UserProfileSerializer,
)
from .models import UserProfile


class SignUpView(APIView):
    @swagger_auto_schema(
        operation_id="회원가입",
        operation_description="회원가입을 진행합니다.",
        request_body=SignUpRequestSerializer,
        responses={201: UserProfileSerializer, 400: "Bad Request"},
    )
    def post(self, request):

        user_serializer = UserSerializer(data=request.data) #요청으로부터 회원가입용 유저 데이터(아이디, 유저네임, 비번, 이메일) 직렬화해서 받아오기
        if user_serializer.is_valid(raise_exception=True): #제대로 UserSerializer 객체가 생겼다면
            user = user_serializer.save() #해당 객체를 기본 User 테이블에 바로 저장하고 일단 불러옴
            user.set_password(user.password) #비밀번호는 평문으로 저장되면 큰일나니까 암호화 필요 -> 유저 객체에 set_password 함수로 지금 평문 비번을 넣어주면 암호화된게 들어감
            user.save() #비번 바뀐 유저 객체를 저장 

        college = request.data.get("college") #요청에서 바로 데이터 뽑기
        major = request.data.get("major")

        user_profile = UserProfile.objects.create( #해당 유저객체를 포함해서 유저프로필 객체를 만들어서 db에 저장
            user=user, college=college, major=major 
        )
        user_profile_serializer = UserProfileSerializer(instance=user_profile) #만들은 유저프로필 객체를 직렬화
        return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED) #직렬화한 유저프로필 객체의 데이터만 빼내서 응답


class SignInView(APIView):
    @swagger_auto_schema(
        operation_id="로그인",
        operation_description="로그인을 진행합니다.",
        request_body=SignInRequestSerializer,
        responses={200: UserSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request):
        # query_params 에서 username, password를 가져온다.
        username = request.data.get("username") #요청에서 바로 유저네임과 비번을 뽑아옴
        password = request.data.get("password")
        if username is None or password is None: #둘중에 하나라도 없다면 뭔가 빠졌다고 에러 리턴
            return Response(
                {"message": "missing fields ['username', 'password'] in query_params"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(username=username) #기본 유저 db에서 유저네임(primary key)이 맞는 유저 뽑아옴
            if not user.check_password(password): #유저 db에 있는 암호화한 비번 vs 요청에 들어있는 평문 비번의 최종일치 여부 판정 -> 비번 틀리면 에러 리턴
                return Response(
                    {"message": "Password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_profile = UserProfile.objects.get(user=user) #해당 유저 객체와 일대일로 매핑되는 유저 프로필 객체를 뽑아옴
            user_profile_serializer = UserProfileSerializer(instance=user_profile) # 그 유저 프로필 객체를 직렬화 해서 그 데이터만 리턴
            return Response(user_profile_serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist: #유저가 없는 에러(장고 유저 객체에서 기본으로 제공) 발생시 에러 리턴
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
