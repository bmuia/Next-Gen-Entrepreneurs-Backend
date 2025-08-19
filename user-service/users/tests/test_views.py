from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UserServiceTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user-register')
        self.token_url = reverse('token-obtain-pair') 
        self.me_url = reverse('current-user')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'testuser@example.com',
            'first_name': 'Test'
            }


    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_admin_registration(self):
        admin_data = self.user_data.copy()
        admin_data['role'] = 'admin'
        response = self.client.post(self.register_url, admin_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_superuser_registration(self):
        superuser_data = self.user_data.copy()
        superuser_data["role"] = 'superuser'
        response = self.client.post(self.register_url, superuser_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        

    def test_token_obtain_pair(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_current_user_authenticated(self):
        self.client.post(self.register_url, self.user_data, format='json')
        token_response = self.client.post(self.token_url, self.user_data, format='json')
        access_token = token_response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_get_current_user_unauthenticated(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
