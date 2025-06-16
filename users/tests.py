from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, UserProfile, GuestProfile
import json


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_user_creation(self):
        """Test user creation and profile auto-creation"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(hasattr(self.user, 'profile'))
        
    def test_profile_has_active_access(self):
        """Test the has_active_access property"""
        profile = self.user.profile
        self.assertFalse(profile.has_active_access)


class UserAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'device_fingerprint': 'test-device-123'
        }
        
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        
    def test_user_login(self):
        """Test user login"""
        # Create a user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Try to login
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Check if device fingerprint was saved
        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.profile.device_fingerprint, 'test-device-123')
        
    def test_device_fingerprint_mismatch(self):
        """Test login with different device fingerprint"""
        # Create a user first
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Login to set initial device fingerprint
        self.client.post(self.login_url, self.login_data, format='json')
        
        # Try to login with different device fingerprint
        different_device_data = self.login_data.copy()
        different_device_data['device_fingerprint'] = 'different-device-456'
        
        response = self.client.post(self.login_url, different_device_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
