from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Объект доступен для изменения только его владельцем или администратором.
    """

    def has_object_permission(self, request, view, obj):
        # Проверка на то, что запрос является безопасным или пользователь является владельцем объекта
        if request.method in SAFE_METHODS:
            return True
        # Позволяет доступ если пользователь - владелец объекта или администратор
        return obj.author == request.user or request.user.is_staff
