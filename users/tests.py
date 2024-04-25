from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import User


class UserManagerTests(TestCase):
    """Тесты для проверки менеджера пользовательских моделей."""

    def test_create_user(self):
        """Проверка создания обычного пользователя"""
        user = User.objects.create_user(email='test@exampleuser.com', first_name='Roman', phone='1234567890',
                                        password='Password567$')
        self.assertEqual(user.email, 'test@exampleuser.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.first_name, 'Roman')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.role, 'user')

    def test_create_superuser(self):
        """Проверка создания суперпользователя"""
        admin_user = User.objects.create_superuser(email='testsuper@user.com', first_name='Super', phone='0987654321',
                                                   password='Password987$')
        self.assertEqual(admin_user.email, 'testsuper@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertEqual(admin_user.first_name, 'Super')
        self.assertEqual(admin_user.phone, '0987654321')
        self.assertEqual(admin_user.role, 'admin')

    def test_create_user_without_email_raises_error(self):
        """Проверка, что создание пользователя без email вызывает ошибку"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, first_name='NoEmail', phone='1234567890', password='Password453$')


class UserModelTests(TestCase):
    """Тесты для модели пользователя."""

    @classmethod
    def setUpTestData(cls):
        """Создание объекта пользователя для тестов"""
        cls.user = User.objects.create_user(email='test@user.com', first_name='Test', phone='1234567890',
                                            password='Password111$')

    def test_user_str(self):
        """Проверка строкового представления модели"""
        self.assertEqual(str(self.user), 'test@user.com')

    def test_user_has_correct_permissions(self):
        """Проверка прав доступа пользователя"""
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)


class PermissionsTests(TestCase):
    """Тесты для пользовательских разрешений."""

    def setUp(self):
        """Инициализация объектов для теста разрешений."""
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Test',
            phone='1234567890',
            password='testpassword',
            role='user'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            first_name='Admin',
            phone='1234567890',
            password='adminpassword'
        )

    def test_is_owner_or_admin_permission(self):
        """Тест на разрешение доступа для владельца и администратора."""
        from .permissions import IsOwnerOrAdmin
        permission = IsOwnerOrAdmin()

        # Создание запроса с аутентификацией пользователя
        request = self.factory.get('/path')
        force_authenticate(request, user=self.user)
        request.user = self.user

        # Проверяем разрешения для пользователя
        result = permission.has_object_permission(request, None, self.user)
        self.assertTrue(result)

        # Проверяем разрешения для администратора
        admin_request = self.factory.get('/path')
        force_authenticate(admin_request, user=self.admin_user)
        admin_request.user = self.admin_user

        admin_result = permission.has_object_permission(admin_request, None, self.user)
        self.assertTrue(admin_result)
