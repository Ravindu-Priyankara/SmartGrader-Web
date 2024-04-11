from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

'''class LoginSignupTestCase(TestCase):
    def setUp(self):
        # Create a test user for login
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_login_view(self):
        # Test login view with correct credentials
        response = self.client.post(reverse('login'), {'mail': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Assuming login success redirects to homepage or another page

        # Test login view with incorrect credentials
        response = self.client.post(reverse('login'), {'mail': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 400)  # Assuming incorrect credentials return status code 400

    def test_signup_view(self):
        # Test signup view with valid data
        response = self.client.post(reverse('signup'), {'f_name': 'Test', 'l_name': 'User', 'mail': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)  # Assuming signup success redirects to another page

        # Test signup view with invalid data (e.g., missing required fields)
        response = self.client.post(reverse('signup'), {'f_name': 'Test', 'l_name': 'User'})
        self.assertEqual(response.status_code, 400)  # Assuming invalid data return status code 400'''

from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            profession='Engineer',
            country='USA',
            number='123456789'
        )

    def test_has_perm(self):
        # Test if the user has a specific permission
        self.assertTrue(self.user.has_perm('webApp.change_customuser'))

    def test_no_perm(self):
        # Test if the user doesn't have a specific permission
        self.assertFalse(self.user.has_perm('webApp.delete_customuser'))

    def test_custom_perm(self):
        # Test a custom permission
        # For example, let's assume your app defines a custom permission called 'can_view_dashboard'
        self.user.user_permissions.add('webApp.can_view_dashboard')
        self.assertTrue(self.user.has_perm('webApp.can_view_dashboard'))

