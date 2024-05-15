from django.urls import path
### 추가
from .views import CommentListView, CommentDetailView
###

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가 #✏️ "": 추가적인 코드가 아무것도 없을 때
    path("<int:comment_id>/", CommentDetailView.as_view()), ### 추가 #✏️뒤에 int가 붙어 올 경우 변수 post_id에 넣음.
]