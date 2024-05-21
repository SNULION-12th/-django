from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.request_serializers import SignInRequestSerializer, SignUpRequestSerializer, TokenRefreshRequestSerializer, SignOutReqeustSerializer

from .serializers import ( #필요한 serializer들을 받아오기 
    UserSerializer,
    UserProfileSerializer,
)
from .models import UserProfile

from rest_framework_simplejwt.tokens import RefreshToken #토큰 발급을 위해서 사용할 클래스의 이름

def generate_token_in_serialized_data(user, user_profile): #유저 객체를 받아서 두 토큰을 발급한 뒤 직렬화 한 데이터를 같이 묶어서 리턴
    token = RefreshToken.for_user(user)
    refresh_token, access_token = str(token), str(token.access_token) #이렇게 되는 이유를 알으려면 RefreshToken 클래스의 작동 원리를 알아야 함
    serialized_data = UserProfileSerializer(user_profile).data
    serialized_data["token"] = {"access": access_token, "refresh": refresh_token}
    return serialized_data

def set_token_on_response_cookie(user, status_code): #유저 객체를 받아서 두 토큰 발급 -> 유저 데이터만 직렬화 해서 응답 객체에 넣은 뒤에 응답 객체 자체에 cookie로 두 토큰을 붙여서 보안성 강화
    token = RefreshToken.for_user(user)
    user_profile = UserProfile.objects.get(user=user)
    serialized_data = UserProfileSerializer(user_profile).data
    res = Response(serialized_data, status=status_code) #status_code를 따로 파라미터로 받아서 200, 201 선택 가능하게 하기
    res.set_cookie("refresh_token", value=str(token), httponly=True)
    res.set_cookie("access_token", value=str(token.access_token), httponly=True)
    return res

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

        #이 위에까지는 jwt 사용과 관계 없이 동일

        #serialized_data = generate_token_in_serialized_data(user, user_profile) #쿠키로 담아 보내기 전
        #return Response(serialized_data, status=status.HTTP_201_CREATED) #쿠키로 담아보내기 전

        return set_token_on_response_cookie(user, status_code = status.HTTP_201_CREATED) #아예 응답 객체 자체를 만들어서 return 

        #user_profile_serializer = UserProfileSerializer(instance=user_profile) #만들은 유저프로필 객체를 직렬화
        #return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED) #직렬화한 유저프로필 객체의 데이터만 빼내서 응답
        

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
            
            return set_token_on_response_cookie(user, status_code=status.HTTP_200_OK)

            #아래는 쿠키에 토큰을 담아서 보내기 전
            #user_profile = UserProfile.objects.get(user=user) #해당 유저 객체와 일대일로 매핑되는 유저 프로필 객체를 뽑아옴
            #serialized_data = generate_token_in_serialized_data(user, user_profile) #jwt 사용해서 토큰 같이 넣어서 직렬화 데이터 생성

            #user_profile_serializer = UserProfileSerializer(instance=user_profile) # 그 유저 프로필 객체를 직렬화 해서 그 데이터만 리턴
            return Response(serialized_data, status=status.HTTP_200_OK)

        except User.DoesNotExist: #유저가 없는 에러(장고 유저 객체에서 기본으로 제공) 발생시 에러 리턴
            return Response(
                {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

class TokenRefreshView(APIView):
    @swagger_auto_schema(
        operation_id="토큰 재발급",
        operation_description="access 토큰을 재발급 받습니다.",
        request_body=TokenRefreshRequestSerializer,
        responses={200: UserProfileSerializer},
    )
    def post(self, request):
        refresh_token = request.data.get("refresh") #request body에서 refresh 토큰 받아옴
        
        #### 1
        if not refresh_token:
            return Response(
                {"detail": "no refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
        #### 2 #refresh 토큰 유효성 검증
            RefreshToken(refresh_token).verify()
        except:
            return Response(
                {"detail": "please signin again."}, status=status.HTTP_401_UNAUTHORIZED
            )
            
        #### 3 #새로운 access_token 발급 후 쿠키로 전달
        new_access_token = str(RefreshToken(refresh_token).access_token)
        response = Response({"detail": "token refreshed"}, status=status.HTTP_200_OK)
        response.set_cookie("access_token", value=str(new_access_token), httponly=True)
        return response

class SignOutView(APIView):
    @swagger_auto_schema(
            operation_id="로그아웃",
            operation_description="사용자를 로그아웃 시킵니다.",
            request_body=SignOutReqeustSerializer,
            responses={401: "Unauthorized", 400: "Bad request", 204: "No content"},
    )
    def post(self, request):
        #refresh token을 블랙리스트에 추가하면 로그아웃이 됨
        #프론트에서는 별개로 저장된 토큰 쿠키들을 삭제해줘야함

        refresh_token=request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "no refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        author = request.user #현재 로그인 되어있는지 확인해야 로그아웃을 시킬 수 있으므로 로그인 여부 검증
        if not author.is_authenticated:
            return Response(
                {"detail": "please signin"}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        try: #이미 토큰이 만료되지는 않았는지 검증
            RefreshToken(refresh_token).verify()
        except:
            return Response(
                {"detail": "please signin again."}, status=status.HTTP_401_UNAUTHORIZED
            )
        
        RefreshToken(refresh_token).blacklist()
        response=Response(status=status.HTTP_204_NO_CONTENT)
        return response
        

