from django.contrib import admin

# Register your models here.
from .models import UserProfile   # 추가

admin.site.register(UserProfile)  # 추가