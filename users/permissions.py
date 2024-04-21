from rest_framework import permissions
from users.models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Пользовательский класс разрешений:
    - Разрешает доступ только аутентифицированным пользователям.
    - Позволяет доступ на редактирование и удаление только владельцам объекта или администраторам.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Проверяем, является ли пользователь администратором или суперпользователем
        if request.user.is_superuser or request.user.role == 'admin':
            return True

        # Проверяем, является ли объект пользователем и совпадает ли он с текущим пользователем
        if isinstance(obj, User):
            return obj == request.user

        return False
