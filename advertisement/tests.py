from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from advertisement.models import Ad, Review

User = get_user_model()


class AdTests(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.user_password = 'Password123#'  # Сохраняем пароль для использования при логине
        self.user = User.objects.create_user(
            email='Testuser@example.com',
            password=self.user_password,  # Используем переменную
            first_name='TestUser',
            phone='1234567890'
        )

        self.admin = User.objects.create_superuser(
            email='Testadmin@example.com',
            password=self.user_password,  # Используем тот же пароль для простоты
            first_name='TestAdmin',
            phone='9876543210'
        )

        self.ad = Ad.objects.create(
            title='Test title',
            price=100,
            description='Test description',
            author=self.user
        )

    def test_list_ads(self):
        """
        Тестирование получения списка объявлений анонимными пользователями.
        """
        url = reverse('advertisement:ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ad_authenticated(self):
        """
        Тестирование создания объявления аутентифицированным пользователем.
        """
        self.client.login(email='Testuser@example.com', password=self.user_password)
        url = reverse('advertisement:ad-list')
        data = {'title': 'New Ad', 'price': 150, 'description': 'Brand new ad'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_update_ad_owner(self):
        """
        Тестирование обновления объявления пользователем, который является владельцем.
        """
        self.client.login(email='Testuser@example.com', password=self.user_password)
        url = reverse('advertisement:ad-detail', kwargs={'pk': self.ad.id})
        data = {'title': 'Updated Ad', 'description': 'Updated description'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_delete_ad_not_owner(self):
        """
        Тестирование попытки удаления объявления администратором, который не является владельцем.
        """

        self.client.login(email='Testadmin@example.com', password='Password123#')
        url = reverse('advertisement:ad-detail', kwargs={'pk': self.ad.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()


class ReviewTests(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.user_password = 'Password123#'
        self.user = User.objects.create_user(
            email='user@example.com',
            password=self.user_password,
            first_name='TestUser',
            phone='1234567890'
        )
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password=self.user_password,
            first_name='Admin',
            phone='9876543210'
        )
        self.ad = Ad.objects.create(
            title='Test Ad',
            price=100,
            description='Test Description',
            author=self.user
        )
        self.review = Review.objects.create(
            text='Test Review',
            author=self.user,
            ad=self.ad
        )

    def test_list_reviews_anonymous(self):
        """
        Анонимные пользователи могут получать список отзывов.
        """
        url = reverse('advertisement:review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_authenticated(self):
        """
        Аутентифицированный пользователь может создать отзыв.
        """
        self.client.login(email='user@example.com', password=self.user_password)
        url = reverse('advertisement:review-list')
        data = {'text': 'New Review', 'ad': self.ad.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_review_owner(self):
        """
        Владелец отзыва может его обновить.
        """
        self.client.login(email='user@example.com', password=self.user_password)
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        data = {'text': 'Updated Review'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_any_review(self):
        """
        Администратор может удалять любые отзывы.
        """
        self.client.login(email='admin@example.com', password=self.user_password)
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_not_owner(self):
        """
        Пользователь, не являющийся владельцем отзыва, не может его удалить.
        """
        # Создание второго пользователя, который не является автором отзыва
        User.objects.create_user(
            email='otheruser@example.com',
            password='OtherPassword123#',
            first_name='OtherUser',
            phone='0987654321'
        )

        self.client.login(email='otheruser@example.com', password='OtherPassword123#')
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
