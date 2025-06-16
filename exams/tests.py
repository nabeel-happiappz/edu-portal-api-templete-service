from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Department, Question, Answer, Exam, ExamAnswer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ExamModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description"
        )
        
        self.question = Question.objects.create(
            department=self.department,
            question_type=1,
            content="Test Question",
            created_by=self.user
        )
        
        self.answer = Answer.objects.create(
            question=self.question,
            text="Test Answer",
            is_correct=True
        )
        
        self.exam = Exam.objects.create(
            user=self.user,
            department=self.department,
            status='active'
        )
    
    def test_department_creation(self):
        """Test department creation"""
        self.assertEqual(self.department.name, "Test Department")
        
    def test_question_creation(self):
        """Test question creation"""
        self.assertEqual(self.question.content, "Test Question")
        self.assertEqual(self.question.department, self.department)
        
    def test_answer_creation(self):
        """Test answer creation"""
        self.assertEqual(self.answer.text, "Test Answer")
        self.assertTrue(self.answer.is_correct)
        self.assertEqual(self.answer.question, self.question)
        
    def test_exam_creation(self):
        """Test exam creation"""
        self.assertEqual(self.exam.user, self.user)
        self.assertEqual(self.exam.department, self.department)
        self.assertEqual(self.exam.status, 'active')


class ExamAPITests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Set up authorization
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create department
        self.department = Department.objects.create(
            name="Test Department",
            description="Test Department Description"
        )
        
        # Create questions and answers
        for i in range(1, 6):
            question = Question.objects.create(
                department=self.department,
                question_type=1,
                content=f"Test Question {i}",
                created_by=self.user
            )
            
            # Create 4 answers for each question, with one correct
            for j in range(1, 5):
                Answer.objects.create(
                    question=question,
                    text=f"Answer {j}",
                    is_correct=(j == 1)  # First answer is correct
                )
        
        # URLs
        self.exams_url = reverse('exam-list')
        
    def test_list_departments(self):
        """Test listing departments"""
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Test Department")
        
    def test_start_exam(self):
        """Test starting an exam"""
        url = reverse('exam-start', args=[0])  # pk is ignored for this endpoint
        data = {'department': self.department.id}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('exam_id', response.data)
        
        # Check that an exam was created
        self.assertEqual(Exam.objects.count(), 1)
        
    def test_get_exam_questions(self):
        """Test getting questions for an exam"""
        # Start an exam first
        exam = Exam.objects.create(
            user=self.user,
            department=self.department,
            status='active'
        )
        
        url = reverse('exam-questions', args=[exam.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that we got all questions
        self.assertEqual(len(response.data), 5)
        
    def test_submit_exam(self):
        """Test submitting answers for an exam"""
        # Start an exam first
        exam = Exam.objects.create(
            user=self.user,
            department=self.department,
            status='active'
        )
        
        # Get questions
        questions = Question.objects.filter(department=self.department)
        
        # Prepare answers (answer all questions correctly)
        answers = []
        for question in questions:
            correct_answer = Answer.objects.get(question=question, is_correct=True)
            answers.append({
                'question_id': question.id,
                'answer_id': correct_answer.id
            })
        
        url = reverse('exam-submit', args=[exam.id])
        data = {'answers': answers}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that score is 100%
        self.assertEqual(response.data['score'], 100.0)
        
        # Check that exam status was updated
        exam.refresh_from_db()
        self.assertEqual(exam.status, 'completed')
        self.assertIsNotNone(exam.end_time)
        
        # Check that answers were recorded
        self.assertEqual(ExamAnswer.objects.count(), 5)
        
    def test_get_exam_results(self):
        """Test getting results for a completed exam"""
        # Create a completed exam
        exam = Exam.objects.create(
            user=self.user,
            department=self.department,
            status='completed',
            score=80.0
        )
        
        # Add some answers
        question = Question.objects.first()
        answer = Answer.objects.get(question=question, is_correct=True)
        
        ExamAnswer.objects.create(
            exam=exam,
            question=question,
            selected_answer=answer,
            is_correct=True
        )
        
        url = reverse('exam-results', args=[exam.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response structure
        self.assertIn('exam', response.data)
        self.assertIn('question_types', response.data)
