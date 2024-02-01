# django-solution
멋쟁이사자처럼 12기 장고 솔루션 레포지토리(운영진용)

# 특이사항
.venv를 gitignore에 넣었습니다
세미나 진행시에는 상관없지만, 만약에 8주차, 9주차에서 solution branch를 clone받고, 해당 파일로 remote를 django-seminar/${name}으로 지정해서 진행할 시 venv 안에 파일들 재설치가 필요합니다

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

