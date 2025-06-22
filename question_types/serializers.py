from rest_framework import serializers
from .models import QuestionType


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['id', 'code', 'name', 'description']
        read_only_fields = ['id']

    def validate_code(self, value):
        # Convert code to uppercase
        return value.upper()
