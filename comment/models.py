from post.models import Post
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'[post: {self.post}] {self.content}'