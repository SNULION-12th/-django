from django.db import models
from django.contrib.auth.models import User #장고에서 제공해주는 기본 유저 모델을 사용(아이디와 유저네임만이 필드로 들어있음)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    #하나의 유저가 하나의 유저프로필만을 갖도록 원투원 모델링 
    #UserProfile의 객체 userprofile1이 User의 객체 user1과 매칭되어 있다면
    # -> userprofile1.user로 user1에 바로 접근 가능 + user1.userprofile로 userprofile1에 바로 접근 가능(User에는 따로 설정 필요 x)
    #User 객체 삭제 시 이 UserProfile 객체도 같이 삭제되도록 옵션
    college = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"id={self.id}, user_id={self.user.id}, college={self.college}, major={self.major}" #UserProfile 모델의 객체의 출력 형식을 지정