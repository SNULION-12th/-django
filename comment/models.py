## models > Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # <- 추가
from post.models import Post

## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)
class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default=timezone.now)