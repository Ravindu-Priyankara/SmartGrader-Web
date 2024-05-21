from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import re
from django.core.files.uploadedfile import SimpleUploadedFile
from PyPDF2 import PdfWriter
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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




# Define test cases for each view

class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

class LoginFormValidateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password123')

    def test_login_form_validate_success(self):
        response = self.client.post(reverse('login_form_validate'), {
            'mail': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status
        # Assuming session key handling logic needs to be corrected
        self.assertIn('session_key', response.url)

    def test_login_form_validate_failure(self):
        response = self.client.post(reverse('login_form_validate'), {
            'mail': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Invalid username or password'})

class SignupViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

class ValidateSignupViewTest(TestCase):
    def test_validate_signup_success(self):
        response = self.client.post(reverse('validate_signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'profession': 'Developer',
            'country': 'Country',
            'mobile_number': '1234567890',
            'password': 'password123',
            'password1': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

    def test_validate_signup_password_mismatch(self):
        response = self.client.post(reverse('validate_signup'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'profession': 'Developer',
            'country': 'Country',
            'mobile_number': '1234567890',
            'password': 'password123',
            'password1': 'password456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'errors': {'__all__': ['Passwords do not match.']}})

class ViewUsersViewTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(email='user1@example.com', password='password123')
        get_user_model().objects.create_user(email='user2@example.com', password='password123')

    def test_view_users(self):
        response = self.client.get(reverse('view_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertContains(response, 'user1@example.com')
        self.assertContains(response, 'user2@example.com')

class DashboardViewTest(TestCase):
    def test_dashboard_with_session_key(self):
        response = self.client.get(reverse('dashboard') + '?session_key=test_key')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'test_key')

    def test_dashboard_without_session_key(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

class UploadFileViewTest(TestCase):
    def test_upload_file_view_get(self):
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def test_upload_file_view_post(self):
        with open('test_file.pdf', 'rb') as pdf_file:
            response = self.client.post(reverse('upload_file'), {
                'file': pdf_file
            })
            # Additional assertions based on the specific logic of file upload
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'dashboard/student.html')

class ContactViewTest(TestCase):
    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/contactus.html')

class AboutViewTest(TestCase):
    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/aboutus.html')

# Ensure you have the necessary imports at the top of the file


# Utility function to create a test PDF file
def create_test_pdf(content):
    buffer = io.BytesIO()
    pdf_writer = PdfWriter()
    pdf_writer.addBlankPage(width=72, height=72)
    pdf_writer.write(buffer)
    return SimpleUploadedFile('test.pdf', buffer.getvalue())

class UploadCodeFileViewTest(TestCase):
    def test_upload_code_file_view_get(self):
        response = self.client.get(reverse('upload_code_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def test_upload_code_file_view_post(self):
        pdf_file = create_test_pdf("Sample PDF content")
        response = self.client.post(reverse('upload_code_file'), {
            'file': pdf_file,
            'file2': pdf_file
        })
        # Additional assertions based on the specific logic of file upload
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/student_code.html')

class CodingAssignmentViewTest(TestCase):
    def test_coding_assignment_view(self):
        response = self.client.get(reverse('coding_assignment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/coding.html')