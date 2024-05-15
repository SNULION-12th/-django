from django.urls import path
from .views import CommentDetailView, CommentListView 

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentListView.as_view()), ### 추가
    path("<int:comment_id>/", CommentDetailView.as_view()), ### 추가

]