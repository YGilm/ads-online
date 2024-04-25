"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="This API provides all backend functionality for the Ads Online platform",

    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[JWTAuthentication],
)

schema_view_tasks = get_schema_view(
    openapi.Info(
        title="Tasks API Documentation",
        default_version='v1',
        description="Detailed documentation of task-related APIs",
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # djoser
    path('auth/', include('djoser.urls')),  # Подключение Djoser
    path('auth/', include('djoser.urls.jwt')),  # Подключение JWT для Djoser

    # users
    path('', include('users.urls', namespace='users')),

    # advertisement
    path('', include('advertisement.urls', namespace='ads')),

    # documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # redoc-tasks
    path('api/redoc-tasks/', schema_view_tasks.with_ui('redoc', cache_timeout=0), name='schema-redoc-tasks'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
