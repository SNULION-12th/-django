from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.
class Comment(models.Model):
  post = models.ForeignKey(Post, null=True, related_name='comments', on_delete=models.CASCADE)
  content = models.TextField()
  author = models.ForeignKey(User, null=True, related_name='comments', on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"author={self.author}, content={self.content}"