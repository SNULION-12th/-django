from django.db import models

### 🔻 이 부분 추가 🔻 ###
class Tag(models.Model):
    content = models.TextField()
### 🔺 이 부분 추가 🔺 ###
