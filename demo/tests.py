from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import GuestProfile
from exams.models import Department, Question, Answer
from .models import DemoSession, DemoAnswer
import json


class DemoAPITests(APITestCase):
    def setUp(self):
        # Create test department
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description"
        )
        
        # Create test questions and answers
        for q_type in range(1, 7):
            for i in range(1, 12):  # Create 11 questions of each type
                question = Question.objects.create(
                    department=self.department,
                    question_type=q_type,
                    content=f"Test Question {q_type}-{i}",
                    created_by=None
                )
                
                # Create 4 answers for each question, with one correct
                for j in range(1, 5):
                    Answer.objects.create(
                        question=question,
                        text=f"Answer {j}",
                        is_correct=(j == 1)  # First answer is correct
                    )
        
        # Demo registration data
        self.register_data = {
            'name': 'Guest User',
            'email': 'guest@example.com',
            'phone': '1234567890',
            'address': '123 Main St',
            'exam_interested': 'Nursing',
            'device_fingerprint': 'test-device-123'
        }
        
        self.register_url = reverse('demo-register')
        self.verify_otp_url = reverse('demo-verify-otp')
        self.questions_url = reverse('demo-questions')
        self.submit_url = reverse('demo-submit')
    
    def test_demo_registration(self):
        """Test guest registration for demo"""
        response = self.client.post(self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GuestProfile.objects.count(), 1)
        self.assertEqual(GuestProfile.objects.get().email, 'guest@example.com')
        
        # Check that OTP was generated
        guest = GuestProfile.objects.get()
        self.assertEqual(len(guest.otp), 6)
        self.assertFalse(guest.otp_verified)
    
    def test_otp_verification(self):
        """Test OTP verification"""
        # Register a guest first
        response = self.client.post(self.register_url, self.register_data, format='json')
        
        # Get the generated OTP
        guest = GuestProfile.objects.get()
        otp = guest.otp
        
        # Verify the OTP
        verify_data = {
            'email': 'guest@example.com',
            'otp': otp
        }
        
        response = self.client.post(self.verify_otp_url, verify_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that OTP is marked as verified
        guest.refresh_from_db()
        self.assertTrue(guest.otp_verified)
        
        # Check that a demo session was created
        self.assertEqual(DemoSession.objects.count(), 1)
        
    def test_get_demo_questions(self):
        """Test getting demo questions"""
        # Register and verify a guest
        response = self.client.post(self.register_url, self.register_data, format='json')
        guest = GuestProfile.objects.get()
        otp = guest.otp
        
        verify_data = {
            'email': 'guest@example.com',
            'otp': otp
        }
        response = self.client.post(self.verify_otp_url, verify_data, format='json')
        session_id = response.data['session_id']
        
        # Get demo questions
        response = self.client.get(f"{self.questions_url}?session_id={session_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that we got questions
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 60)  # 10 questions of each type
        
    def test_submit_demo_answers(self):
        """Test submitting demo answers"""
        # Register and verify a guest
        response = self.client.post(self.register_url, self.register_data, format='json')
        guest = GuestProfile.objects.get()
        otp = guest.otp
        
        verify_data = {
            'email': 'guest@example.com',
            'otp': otp
        }
        response = self.client.post(self.verify_otp_url, verify_data, format='json')
        session_id = response.data['session_id']
        
        # Get demo questions
        response = self.client.get(f"{self.questions_url}?session_id={session_id}")
        questions = response.data['questions']
        
        # Prepare answers (just answer the first 10 questions)
        answers = []
        for i in range(10):
            question = questions[i]
            answers.append({
                'question_id': question['id'],
                'answer_id': question['answers'][0]['id']  # Select first answer (correct)
            })
        
        # Submit answers
        submit_data = {
            'session_id': session_id,
            'answers': answers
        }
        
        response = self.client.post(self.submit_url, submit_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that demo is marked as used
        guest.refresh_from_db()
        self.assertTrue(guest.demo_used)
        self.assertEqual(guest.demo_questions_attempted, 10)
        
        # Check that answers were recorded
        self.assertEqual(DemoAnswer.objects.count(), 10)
        
        # Check score
        self.assertEqual(response.data['total_questions'], 10)
        self.assertEqual(response.data['correct_answers'], 10)  # All answers were correct
        self.assertEqual(response.data['score_percentage'], 100.0)
