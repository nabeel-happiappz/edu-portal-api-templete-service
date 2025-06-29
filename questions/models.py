from django.db import models
from django.contrib.auth import get_user_model
from question_types.models import QuestionType

User = get_user_model()


class Question(models.Model):
    """
    Model for managing educational questions with various question types
    """
    question_type = models.TextField()
    content = models.TextField()
    image_url = models.TextField(blank=True, null=True)
    options = models.JSONField()
    correct_answer = models.JSONField()
    explanation = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text='Duration in minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.TextField()
    courses = models.JSONField()
    roles = models.JSONField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question_type}: {self.content[:50]}..."

    class Meta:
        ordering = ['-created_at']
