from django.urls import path
### 추가
from .views import CommentListView, CommentDetailView
###

app_name = 'comments'
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가
    path("<int:comment_id>/", CommentDetailView.as_view())
]