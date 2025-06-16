from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import GuestProfile, DeviceLock
from exams.models import Department, Question, Answer, Exam, ExamAnswer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AdminAPITests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpassword123'
        )
        
        # Set up authorization for admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create test data
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description"
        )
        
        self.question = Question.objects.create(
            department=self.department,
            question_type=1,
            content="Test Question",
            created_by=self.admin_user
        )
        
        self.answer = Answer.objects.create(
            question=self.question,
            text="Test Answer",
            is_correct=True
        )
        
        self.exam = Exam.objects.create(
            user=self.regular_user,
            department=self.department,
            status='completed',
            score=85.0
        )
        
        ExamAnswer.objects.create(
            exam=self.exam,
            question=self.question,
            selected_answer=self.answer,
            is_correct=True
        )
        
        self.guest = GuestProfile.objects.create(
            name="Guest User",
            email="guest@example.com",
            demo_used=True,
            demo_questions_attempted=10
        )
        
        self.device_lock = DeviceLock.objects.create(
            user=self.regular_user,
            device_fingerprint="test-device-123",
            is_locked=True,
            locked_reason="Test lock"
        )
    
    def test_admin_department_list(self):
        """Test admin can list departments"""
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_admin_user_list(self):
        """Test admin can list users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_reset_device(self):
        """Test admin can reset device fingerprint"""
        url = reverse('admin-reset-device', args=[self.regular_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that device fingerprint was reset
        self.regular_user.profile.refresh_from_db()
        self.assertEqual(self.regular_user.profile.device_fingerprint, '')
        
        # Check that device lock was unlocked
        self.device_lock.refresh_from_db()
        self.assertFalse(self.device_lock.is_locked)
    
    def test_reset_demo(self):
        """Test admin can reset demo status"""
        url = reverse('admin-reset-demo', args=[self.guest.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that demo status was reset
        self.guest.refresh_from_db()
        self.assertFalse(self.guest.demo_used)
        self.assertEqual(self.guest.demo_questions_attempted, 0)
    
    def test_unlock_device(self):
        """Test admin can unlock device"""
        url = reverse('admin-unlock-device', args=[self.device_lock.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that device was unlocked
        self.device_lock.refresh_from_db()
        self.assertFalse(self.device_lock.is_locked)
        self.assertEqual(self.device_lock.locked_reason, '')
    
    def test_participation_report(self):
        """Test admin can get participation report"""
        url = reverse('admin-participation-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check report structure
        self.assertIn('date_range', response.data)
        self.assertIn('total_users', response.data)
        self.assertIn('department_breakdown', response.data)
    
    def test_pass_rate_report(self):
        """Test admin can get pass rate report"""
        url = reverse('admin-pass-rate-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check report structure
        self.assertIn('date_range', response.data)
        self.assertIn('total_exams', response.data)
        self.assertIn('department_breakdown', response.data)
        self.assertIn('question_type_breakdown', response.data)
    
    def test_csv_report(self):
        """Test admin can get CSV report"""
        url = reverse('admin-participation-report') + '?format=csv'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="participation_report.csv"', response['Content-Disposition'])
    
    def test_excel_report(self):
        """Test admin can get Excel report"""
        url = reverse('admin-pass-rate-report') + '?format=excel'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename="pass_rate_report.xlsx"', response['Content-Disposition'])
