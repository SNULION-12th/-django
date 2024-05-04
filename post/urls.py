from django.urls import path
### view파일에서 선언한 2개의 
from .views import PostListView, PostDetailView
###

app_name = 'post'
urlpatterns = [
    # CBV url path
    # /api/~~/ 더 이상 아무것도 붙지 않으면 post list view를 쓰겠다.
    path("", PostListView.as_view()), ### 추가
    # integer 변수를 post_id 변수에 넣겠다.
    # view.py 에서 post_id를 쓸 수 있는 이유가 되는 문장 1개
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가

]