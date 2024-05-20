from django.urls import path
from .views import CommentView, CommentDetailView

app_name = 'comment'
urlpatterns = [
    # CBV url path
    path("", CommentView.as_view()),
    path("<int:comment_id>/", CommentDetailView.as_view()),
]