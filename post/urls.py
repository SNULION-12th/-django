from django.urls import path
from .views import PostListView, PostDetailView # 정의한 두 개의 view 클래스를 import

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가
]