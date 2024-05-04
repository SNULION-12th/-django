from django.urls import path
from .views import PostListView, PostDetailView

## post app의 주소를 설정하는데
app_name = 'post'
urlpatterns = [
		## path가 비어있으면 PostListView를 실행시킬거야~
    path("", PostListView.as_view()),
    
    ## path에 int가 들어오면 그걸 post_id라는 변수로 저장한 후, 
    ## postDetailView를 실행시킬거야~
    path("<int:post_id>/", PostDetailView.as_view())
]