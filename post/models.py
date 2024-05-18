## models > Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해 timezone 가져옴~
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag

## Post라는 class를 선언해줍니다
## (models.Model을 상속받으면 models.Model이 가지는 정보를 모두 가지게되겠죠?)
class Post(models.Model):
		## title은 최대 256자의 character!
    title = models.CharField(max_length=256) #--post의 최대 길이
    
    ## content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    ## created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now) #--날짜를 가져오는 기능. 생성될 때 현재 시간이 변수에 자동으로 저장됨.

    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE) #-- One To Many for Users  
    #-- 한쪽에만 설정하면 됨. Post 에다가 author = ... 을 mapping만 하면 된다. User 에 들어가서 또 설정해줄 필요 x

    like_users = models.ManyToManyField(User, blank=True, related_name='like_posts', through='Like') #-- One to Many 구현 for likes
    #-- through 지정?

    tags = models.ManyToManyField(Tag, blank=True, related_name='posts') #--one to many for tags
    

		## 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title
    

class Like(models.Model):
    #--like 하나당 user, post, 시간이 mapping 된다
    user = models.ForeignKey(User, on_delete=models.CASCADE) #foreign key -- many-to-many
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #foreign key -- many-to-many
    created_at = models.DateTimeField(default=timezone.now)
#-- Thus, a many-to-many field
#-- null=True: null 값으로 지정되어도 된다?
#-- blank=True: like users 가 비어져 있어도 괜찮다