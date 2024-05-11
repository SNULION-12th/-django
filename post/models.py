from django.db import models
from tag.models import Tag

# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone
from django.contrib.auth.models import User


## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)
class Post(models.Model):
		## title은 최대 256자의 character!
    title = models.CharField(max_length=256)
    
    #왜 이건 따로 App으로 안만들어도 되는가? "관계"중에 자동으로 생기는 것이기 때문. 새로 이걸 저장할 Class가 필요하지 않다.
    ##Blank = true (비어져 있어도 High-Level 검사 상 빈칸가능)
    like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')    
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    ##Author을 Foreign Key로 가져온다는 뜻, 기본값이 False인데 null=True일 경우 빈칸 가능, ㅊ
    
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title
      
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
