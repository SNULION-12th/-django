from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
	path("", PostListView.as_view()),
	path("<int:post_id>/", PostDetailView.as_view()), #as_view()로 라우팅 해주는듯?
	#seminar 전체의 url에서 /api/post로 시작하는 요청은 여기로 라우팅
	#여기서 path parameter를 위의 구조로 지정하면, 패스 파라미터 사용 가능
	#api/post/1 과 같은 형식으로 가면 아래의 라우터를 따라서 작동
]