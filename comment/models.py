from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
	author = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.content
