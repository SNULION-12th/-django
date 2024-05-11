from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), 
    path("<int:post_id>/", PostDetailView.as_view()), #post_id 가 Parameter로 오면 PostDetailView 함수로 처리해라

]