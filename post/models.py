from django.db import models
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField()
	created_at = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.title # 해당 객체를 print 시 title 정보만 반환
