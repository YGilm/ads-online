from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from advertisement.models import Ad, Review

User = get_user_model()


class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='Testuser@example.com', password='Password123#',
                                             first_name='TestUser', phone='1234567890')
        self.admin = User.objects.create_superuser(email='Testadmin@example.com', password='Password123#',
                                                   first_name='TestAdmin', phone='9876543210')
        self.ad = Ad.objects.create(title='Test title', price=100, description='Test description', author=self.user)
        self.user_token = RefreshToken.for_user(self.user).access_token
        self.admin_token = RefreshToken.for_user(self.admin).access_token

    def set_auth_header(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_ads(self):
        """Проверка получения списка объявлений анонимными пользователями."""
        url = reverse('advertisement:ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ad_authenticated(self):
        """Проверка создания объявления аутентифицированным пользователем."""
        self.set_auth_header(self.user_token)
        url = reverse('advertisement:ad-list')
        data = {'title': 'New Ad', 'price': 150, 'description': 'Brand new ad'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ad_owner(self):
        """Проверка обновления объявления пользователем, который является его владельцем."""
        self.set_auth_header(self.user_token)
        url = reverse('advertisement:ad-detail', kwargs={'pk': self.ad.id})
        data = {'title': 'Updated Ad', 'description': 'Updated description'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ad_not_owner(self):
        """Проверка удаления объявления администратором, не являющимся владельцем объявления."""
        self.set_auth_header(self.admin_token)
        url = reverse('advertisement:ad-detail', kwargs={'pk': self.ad.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='Password123#', first_name='TestUser',
                                             phone='1234567890')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='Password123#',
                                                   first_name='Admin', phone='9876543210')
        self.ad = Ad.objects.create(title='Test Ad', price=100, description='Test Description', author=self.user)
        self.review = Review.objects.create(text='Test Review', author=self.user, ad=self.ad)
        self.user_token = RefreshToken.for_user(self.user).access_token
        self.admin_token = RefreshToken.for_user(self.admin).access_token

    def set_auth_header(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_reviews_anonymous(self):
        """Анонимные пользователи могут получать список отзывов."""
        url = reverse('advertisement:review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_authenticated(self):
        """Аутентифицированный пользователь может создать отзыв."""
        self.set_auth_header(self.user_token)
        url = reverse('advertisement:review-list')
        data = {'text': 'New Review', 'ad': self.ad.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_review_owner(self):
        """Владелец отзыва может его обновить."""
        self.set_auth_header(self.user_token)
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        data = {'text': 'Updated Review'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_any_review(self):
        """Администратор может удалять любые отзывы."""
        self.set_auth_header(self.admin_token)
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_not_owner(self):
        """Пользователь, не являющийся владельцем отзыва, не может его удалить."""
        another_user = User.objects.create_user(email='otheruser@example.com', password='OtherPassword123#',
                                                first_name='OtherUser', phone='0987654321')
        another_user_token = RefreshToken.for_user(another_user).access_token
        self.set_auth_header(another_user_token)
        url = reverse('advertisement:review-detail', kwargs={'pk': self.review.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
