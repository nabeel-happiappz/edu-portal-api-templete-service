from rest_framework import serializers
from .models import Question
from question_types.serializers import QuestionTypeSerializer


class QuestionSerializer(serializers.ModelSerializer):
    question_type_details = QuestionTypeSerializer(source='question_type', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'question_type', 'question_type_details', 'content', 'options',
            'correct_answer', 'explanation', 'duration', 'created_at', 
            'updated_at', 'department', 'courses', 'roles'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
