from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE) #foreign key -- many-to-many
  content = models.TextField()
  author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
