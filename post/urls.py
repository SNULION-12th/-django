from django.urls import path
### 추가
from .views import PostListView, PostDetailView, LikeView
###

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), #--url 뒤에 아무것도 없으면 PostListView로 이동
    path("<int:post_id>/", PostDetailView.as_view()), #-- url 뒤에 post_id 가 있으면 PostDetailView로 이동
    path("<int:post_id>/like/", LikeView.as_view()),
]