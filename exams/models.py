from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    """
    Model for departments/subjects
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Model for exam questions
    """
    QUESTION_TYPES = (
        (1, 'Multiple Choice'),
        (2, 'True/False'),
        (3, 'Fill in the Blanks'),
        (4, 'Matching'),
        (5, 'Sequence'),
        (6, 'Case Study'),
    )
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='questions')
    question_type = models.IntegerField(choices=QUESTION_TYPES)
    content = models.TextField()
    media_url = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_question_type_display()}: {self.content[:50]}..."


class Answer(models.Model):
    """
    Model for question answers
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return f"{self.text[:50]} - {status}"


class Exam(models.Model):
    """
    Model for user exams
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exams')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='exams')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.department.name} - {self.status}"


class ExamAnswer(models.Model):
    """
    Model for user answers in an exam
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('exam', 'question')
    
    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return f"{self.exam.user.email} - Q{self.question.id} - {status}"
