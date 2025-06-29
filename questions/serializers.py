from rest_framework import serializers
from .models import Question
from question_types.serializers import QuestionTypeSerializer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'question_type', 'content', 'image_url', 'options',
            'correct_answer', 'explanation', 'duration', 'created_at',
            'updated_at', 'department', 'courses', 'roles'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
