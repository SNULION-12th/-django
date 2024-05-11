from django.urls import path
from .views import PostListView, PostDetailView, LikeView

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),
    path("<int:post_id>/like/", LikeView.as_view()),
]