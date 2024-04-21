from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import AdvertisementConfig
from .views import ReviewViewSet, AdList, AdDetail

app_name = AdvertisementConfig.name

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Ad generics
    path('ads/', AdList.as_view(), name='ad-list'),
    path('ads/<int:pk>/', AdDetail.as_view(), name='ad-detail'),
]
