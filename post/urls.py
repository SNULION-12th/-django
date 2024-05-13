from django.urls import path
<<<<<<< HEAD
### 추가
from .views import PostListView, PostDetailView, LikeView
###

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()),
    path("<int:post_id>/like/", LikeView.as_view()),
=======
# from .views import ReadAllPostView, CreatePostView
from .views import PostListView, PostDetailView


app_name = 'post'
urlpatterns = [
    # FBV url path
    # path("register_post/", CreatePostView),
    # path("see_post/", ReadAllPostView),
  
    # CBV url path
    path("", PostListView.as_view()),
    path("<int:post_id>/", PostDetailView.as_view()), 
>>>>>>> fb50bd764cbec7a56688593b44ce28f451dd53e0
]