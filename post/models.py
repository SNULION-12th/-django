from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from tag.models import Tag
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=256)
	content = models.TextField()
	created_at = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	#User와 Post는 OnetoMany 관계
	#User이 one이므로 Post에 user의 primary key를 foreign key로 넣어줌
	#null이 true라면 해당 필드는 널 값을 가질 수 있음
	#User 객체가 삭제된다면 해당 Post 객체도 같이 삭제되도록 설정
	#related_name을 지정해주지 않았으므로 User에는 자동으로 post_set이라는 post에 접근 가능한 필드가 생김
	like_users = models.ManyToManyField(User,blank=True,related_name='like_posts',through='Like')
	#manytomany로 연관관계 지정(through model 지정까지 제대로)
	#null과 blank는 다르다! 
	#related_name을 통해 User 객체에서도 이 Post에 접근 가능(User 객체의 필드로 related_name이 자동 생성)
	tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
	#through model 없이 관계 지정했으므로 자동으로 생성됨 
	#tag 모델에도 posts라는 필드가 자동으로 생성됨
	def __str__(self):
		return self.title # 해당 객체를 print 시 title 정보만 반환
	
class Like(models.Model): #manytomany 관계의 through model을 직접 정의(직접 정의 안하면 자동으로 생성된다고 함)
    user = models.ForeignKey(User, on_delete=models.CASCADE) #외래키 두개만 정의
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now) #내가 원하는 필드를 더 넣을 수 있다는게 직접 정의의 장점 