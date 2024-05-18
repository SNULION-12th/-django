from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.

class Comment(models.Model):

    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.content