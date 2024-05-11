from django.urls import path
from .views import  PostListView, PostDetailView, LikeView



app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### id가 url에 붙어서 오면 postdetailview class를 사용하겠다. 
    path("<int:post_id>/like/", LikeView.as_view()),
]