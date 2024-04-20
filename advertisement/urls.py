from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import AdvertisementConfig
from .views import AdViewSet, ReviewViewSet

app_name = AdvertisementConfig.name

router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
