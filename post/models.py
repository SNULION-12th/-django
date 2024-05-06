from django.db import models

from django.utils import timezone
# Create your models here.


class Post(models.Model):
  ##title 최대길이 256, 필요로 하는 데이터 타입(Field class 참조) Char
  title = models.CharField(max_length=256)

  ##TextField 필요 (길이제한 없는 문자열)
  content = models.TextField()

  ## created_at은 현재 시간으로 자동 입력되게
  created_at = models.DateTimeField(default=timezone.now)

  ##print하면 타이틀을 반환, 인스턴스 데이터를 직접 이용하고 싶을때!!
  def __str__(self):
    return self.title