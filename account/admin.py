from django.contrib import admin
from .models import UserProfile   # 추가

admin.site.register(UserProfile)  # 추가