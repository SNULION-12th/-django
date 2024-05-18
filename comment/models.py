from django.db import models
from django.contrib.auth.models import User
from post.models import Post


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content