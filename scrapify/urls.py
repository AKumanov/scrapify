from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Scrapify',
        default_version='v1',
        description="test"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    re_path(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')),
]
