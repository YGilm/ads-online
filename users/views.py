from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwnerOrAdmin
from users.paginators import UserPagination
from users.serializers import CustomUserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = UserPagination

    def perform_create(self, serializer):
        serializer.save()
