from django.urls import path
from .views import CommentListView, CommentDetailView
##views에서 클래스 구현 

app_name = 'comment'
urlpatterns = [
    path("", CommentListView.as_view()),
    path("<int:comment_id>/", CommentDetailView.as_view())
]