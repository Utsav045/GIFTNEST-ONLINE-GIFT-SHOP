from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_user_registration_view(self):
        """Test user registration view"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        
    def test_user_login_view(self):
        """Test user login view"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
    def test_user_login_valid_credentials(self):
        """Test user login with valid credentials"""
        response = self.client.post(
            reverse('users:login'),
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Should be redirected to home page after login
        self.assertContains(response, 'Logout')
        
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        response = self.client.post(
            reverse('users:login'),
            {
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        self.assertEqual(response.status_code, 200)
        # Should show error message (check actual error message in template)
        self.assertContains(response, 'Login')
        
    def test_user_logout(self):
        """Test user logout"""
        # First login
        self.client.login(username='testuser', password='testpass123')
        
        # Then logout
        response = self.client.get(reverse('users:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        # Should be redirected to home page
        self.assertContains(response, 'Login')
        
    def test_user_profile_view_authenticated(self):
        """Test user profile view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        
    def test_user_profile_view_unauthenticated(self):
        """Test user profile view when not authenticated"""
        response = self.client.get(reverse('users:profile'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        
    def tearDown(self):
        """Clean up test data"""
        User.objects.all().delete()