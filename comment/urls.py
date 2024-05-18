from django.urls import path
### 추가
# from .views import ReadAllPostView, CreatePostView, PostListView, PostDetailView
from .views import CommentListView, CommentDetailView
###

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가
    path("<int:comment_id>/", CommentDetailView.as_view()), ### ç추가
]