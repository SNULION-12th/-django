from django.db import models

# Create your models here.
from django.utils import timezone
from post.models import Post
from django.contrib.auth.models import User

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.content