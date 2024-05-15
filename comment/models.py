from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.content
