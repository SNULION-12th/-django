from django.urls import path
from .views import PostCommentView, CommentDetailView
                  ## post번호 주면 조회 및 생성 / 한개의 Comment Modify(delete, update)

app_name = 'comment'
urlpatterns = [
    path("", PostCommentView.as_view()), ##get commentsList by postID(postID query parameter로 받기), create
    path("<int:comment_id>",CommentDetailView.as_view()) ##update, delete
]
