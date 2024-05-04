## models > Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone

## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)
class Post(models.Model):
		## title은 최대 256자의 character!
    title = models.CharField(max_length=256)
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title