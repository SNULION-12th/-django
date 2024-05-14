from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

class Comment(models.Model):
  # Post 1개에 Comment 여러개, One-to-Many 관계
  # User 1개가 Comment 여러개 작성 가능, One-to-Many 관계
  post = models.ForeignKey(Post, related_name="comment_list", on_delete=models.CASCADE)
  content = models.TextField()
  author = models.ForeignKey(User, related_name="comment_list", on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.content