# swagger imports
# import는 맨 위에서~
from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger settings
schema_view = get_schema_view(
    openapi.Info(
        title="LIKELION Blog API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

## 여긴 기존 코드가 존재합니다
## swagger path만 추가하기!
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post/', include('post.urls')),
    # swagger path
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]