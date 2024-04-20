from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, phone, password, role="user"):
        """Создает и сохраняет нового пользователя с заданным email, именем, телефоном, паролем и ролью."""
        if not email:
            raise ValueError('Пользователь должен иметь email')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            phone=phone,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, phone, password):
        """Создает и сохраняет нового суперпользователя с заданным email, именем, телефоном и паролем."""
        user = self.create_user(
            email,
            first_name=first_name,
            phone=phone,
            password=password,
            role="admin"
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Основная модель пользователя для системы аутентификации.

    Использует email в качестве уникального идентификатора. Данная модель предоставляет
    базовые поля, необходимые для аутентификации и управления пользователями, включая
    специальные поля для ролей и статуса активности.
    """
    username = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='имя', **NULLABLE)
    phone = models.CharField(max_length=15, verbose_name='телефон', **NULLABLE)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')],
                            verbose_name='роль')
    image = models.ImageField(upload_to='user_images/', verbose_name='аватар', **NULLABLE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone', 'role']

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email
