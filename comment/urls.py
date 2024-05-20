from django.urls import path
from .views import CommentListView, CommentDetailView

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path('', CommentListView.as_view(), name='comment_list'),
    path("<int:commentId>", CommentDetailView.as_view()),
]