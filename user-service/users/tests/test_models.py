# users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='user'
        )

    def test_user_creation(self):
        """Test that a user is correctly created"""
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.role, 'user')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        """Test the string representation of the user"""
        # Usually User.__str__ returns the email
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_user_role_choices(self):
        """Test user role is valid"""
        valid_roles = ['user', 'admin', 'superuser'] 
        self.assertIn(self.user.role, valid_roles)


