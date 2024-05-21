from django.urls import path
# from .views import ReadAllPostView, CreatePostView
from .views import PostListView, PostDetailView, LikeView, CommentListView, CommentDetailView


app_name = 'post'
urlpatterns = [
    # FBV url path
    # path("register_post/", CreatePostView),
    # path("see_post/", ReadAllPostView),
  
    # CBV url path
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()), 
    path("<int:post_id>/like/", LikeView.as_view()),
    path("<int:post_id>/comment/", CommentListView.as_view()),
    path("<int:post_id>/comment/<int:comment_id>/", CommentDetailView.as_view())
]