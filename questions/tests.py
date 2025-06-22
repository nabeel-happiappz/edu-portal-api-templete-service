from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Question
from question_types.models import QuestionType
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Create question type
        self.question_type = QuestionType.objects.create(
            code='MCQ',
            name='Multiple Choice Question',
            description='A question with multiple choices'
        )

        # Create question
        self.question = Question.objects.create(
            question_type=self.question_type,
            content='Test Question',
            options={"options": ["Option 1", "Option 2", "Option 3", "Option 4"]},
            correct_answer={"answer": "Option 2"},
            explanation="This is a test explanation",
            duration=5,
            department="Nursing",
            courses=["Basic Nursing"],
            roles=["Student"]
        )

        self.question_url = reverse('questions-detail', args=[self.question.id])
        self.question_list_url = reverse('questions-list')

    def test_get_all_questions(self):
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        data = {
            "question_type": self.question_type.id,
            "content": "New Test Question",
            "options": {"options": ["Option A", "Option B", "Option C", "Option D"]},
            "correct_answer": {"answer": "Option C"},
            "explanation": "New explanation",
            "duration": 10,
            "department": "Medicine",
            "courses": ["General Medicine"],
            "roles": ["Student", "Instructor"]
        }
        response = self.client.post(self.question_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_valid_question(self):
        response = self.client.get(self.question_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question(self):
        data = {
            "content": "Updated Question Content",
            "question_type": self.question_type.id,
            "options": {"options": ["Updated Option 1", "Updated Option 2"]},
            "correct_answer": {"answer": "Updated Option 1"},
            "duration": 7,
            "department": "Nursing",
            "courses": ["Advanced Nursing"],
            "roles": ["Student"]
        }
        response = self.client.put(self.question_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        response = self.client.delete(self.question_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify soft delete
        self.assertTrue(Question.objects.get(id=self.question.id).is_deleted)
