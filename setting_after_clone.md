# django-solution
멋쟁이사자처럼 12기 장고 솔루션 레포지토리(운영진용)

# 특이사항
세미나 진행시에는 상관없지만, 만약에 8주차, 9주차에서 solution branch를 clone받고, 해당 파일로 remote를 django-seminar/${name}으로 지정해서 진행할 시(자신의 코드로 진행하는게 아니라 솔루션 받아서 할 때) venv 안에 파일들 재설치 및 migration이 필요합니다. 이를 위해서는 다음 명령어를 순차적으로 실행시키면 됩니다. 8주차, 9주차 solution 코드 작성 위해서 클론받아도 똑같습니다.

# clone받고 터미널에 실행시킬 명령어(순차적으로 하면됩니다)
python -m venv .venv  
.venv\Scripts\activate (venv 켜기 - **mac과 window간에 명령어 다릅니다)  
pip install -r requirements.txt  
python manage.py migrate

# swagger 사용방법
swagger 홈페이지 url은 http://127.0.0.1:8000/swagger/ 입니다.  
기본 세팅은 완료해두었습니다. 일단 권한은 allowany로 해두었습니다. 9주차 세미나팀에서 권한 관련 세미나 내용 진행하면서 이 부분 설정을 바꿔도 될 것 같아요.

swagger 사용 예시는 다음과 같습니다. 각 view method 위에 swagger auto schema를 넣어주시면 됩니다. 더 많은 사용 예시는 post/views.py에서 확인 가능합니다.

```   
@swagger_auto_schema(   
            operation_id='게시글 생성',   
            operation_description='게시글을 생성합니다.',   
            request_body=PostSerializer,   
            responses={201: PostSerializer}
    )
```
* operation_id : api 이름
* operation_description : api 상세 설명
* request_body (optional) : request body에 데이터가 들어가는 경우 여기에 각 데이터의 serializer를 넣어주면 swagger에서 body에 들어가야 할 데이터 형식을 확인할 수 있습니다.
* responses : 가능한 response들을 dictionary 형태로 넣어줍니다. 만약 특정 데이터가 list로 출력된다면 PostSerializer(many=ture)와 같은 형태로 사용 가능합니다.

### 궁금한 점은 minhouu에게 질문해주세요

### .env 파일에 들어갈 secret key는 백엔드 팀 톡방 공지에 올라가있씁니다~