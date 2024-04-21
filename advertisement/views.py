from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Ad, Review
from .permissions import IsOwnerOrAdmin
from .serializers import AdSerializer, ReviewSerializer
from .filters import AdFilter
from .paginators import AdPagination


class AdList(ListCreateAPIView):
    """
    Представление для списка объявлений и создания нового объявления.
    Поддерживает фильтрацию, пагинацию и создание объявления с автоматическим назначением автора.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    pagination_class = AdPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdDetail(RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления конкретного объявления.
    Обеспечивает детальный просмотр, редактирование и удаление объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с отзывами на объявления.
    Поддерживает создание, просмотр, редактирование и удаление отзывов.
    Автоматически назначает автора отзыва при создании.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
