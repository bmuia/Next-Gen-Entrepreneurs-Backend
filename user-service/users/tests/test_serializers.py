from rest_framework.test import APITestCase
from users.serializers import RegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserServiceSerializerTest(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'role': 'user'
        }

    def test_registration_serializer(self):
        serializer = RegistrationSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)  
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.role, self.user_data['role'])
