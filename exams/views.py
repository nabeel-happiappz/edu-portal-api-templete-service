from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .models import Department, Question, Answer, Exam, ExamAnswer
from .serializers import (
    DepartmentSerializer, QuestionSerializer, AnswerSerializer,
    ExamSerializer, ExamDetailSerializer, ExamCreateSerializer,
    ExamSubmitSerializer, ExamResultsSerializer
)
from users.permissions import IsOwnerOrAdmin


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing departments
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for exam management
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Exam.objects.all()
        return Exam.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamDetailSerializer
        elif self.action == 'create' or self.action == 'start':
            return ExamCreateSerializer
        elif self.action == 'results':
            return ExamResultsSerializer
        return ExamSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """
        Start a new exam
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if user has an active exam
        active_exams = Exam.objects.filter(
            user=request.user,
            status='active'
        )
        
        if active_exams.exists():
            return Response({
                "message": "You already have an active exam. Please finish it first."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new exam
        exam = serializer.save(user=request.user)
        
        return Response({
            "message": "Exam started successfully.",
            "exam_id": exam.id
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """
        Get questions for an exam
        """
        exam = self.get_object()
        
        if exam.status != 'active':
            return Response({
                "message": f"This exam is {exam.status}. Cannot retrieve questions."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get questions for the department
        questions = Question.objects.filter(department=exam.department)
        
        # Serialize questions
        serializer = QuestionSerializer(questions, many=True)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit answers for an exam
        """
        exam = self.get_object()
        
        if exam.status != 'active':
            return Response({
                "message": f"This exam is {exam.status}. Cannot submit answers."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExamSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        answers_data = serializer.validated_data.get('answers')
        correct_answers = 0
        total_answers = len(answers_data)
        
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            answer_id = answer_data.get('answer_id')
            
            try:
                question = Question.objects.get(id=question_id, department=exam.department)
                answer = Answer.objects.get(id=answer_id, question=question)
                
                # Check if the answer is correct
                is_correct = answer.is_correct
                if is_correct:
                    correct_answers += 1
                
                # Save the answer
                ExamAnswer.objects.create(
                    exam=exam,
                    question=question,
                    selected_answer=answer,
                    is_correct=is_correct
                )
                
            except (Question.DoesNotExist, Answer.DoesNotExist):
                # Skip invalid questions/answers
                continue
        
        # Calculate score
        score = (correct_answers / total_answers * 100) if total_answers > 0 else 0
        
        # Update exam
        exam.status = 'completed'
        exam.end_time = timezone.now()
        exam.score = score
        exam.save()
        
        return Response({
            "message": "Exam submitted successfully.",
            "score": score
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        Get results for a completed exam
        """
        exam = self.get_object()
        
        if exam.status != 'completed':
            return Response({
                "message": f"This exam is {exam.status}. No results available."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(exam)
        
        # Get question-type breakdown
        question_types = ExamAnswer.objects.filter(exam=exam).values(
            'question__question_type'
        ).annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True))
        )
        
        # Format the response
        question_type_results = []
        for qt in question_types:
            q_type = qt['question__question_type']
            total = qt['total']
            correct = qt['correct']
            q_type_name = dict(Question.QUESTION_TYPES).get(q_type, 'Unknown')
            
            question_type_results.append({
                'type': q_type,
                'name': q_type_name,
                'total': total,
                'correct': correct,
                'percentage': round((correct / total) * 100, 2) if total > 0 else 0
            })
        
        return Response({
            'exam': serializer.data,
            'question_types': question_type_results
        })
