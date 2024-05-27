from django.contrib import admin
from .models import Like, Post

admin.site.register(Post) #-admin page (관리자 페이지)랑 이 앱들이랑 연결하기
admin.site.register(Like)