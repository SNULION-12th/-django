from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'post'
urlpatterns = [
    # CBV url path
    path("", PostListView.as_view()), ### 추가
    path("<int:post_id>/", PostDetailView.as_view()), ### 추가

]