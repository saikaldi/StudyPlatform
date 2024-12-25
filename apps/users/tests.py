from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'phone_number': '1234567890',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_login_user(self):
        # Создаем пользователя
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            phone_number='1234567890',
            password='testpassword'
        )
        # Убедитесь, что URL правильный
        url = reverse('token_obtain_pair')  # Проверьте, что это правильный URL для получения токена
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class TokenTests(APITestCase):
    def test_obtain_token(self):
        # Создаем пользователя
        user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            phone_number='1234567890',
            password='testpassword'
        )
        
        # Проверяем получение токена
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
