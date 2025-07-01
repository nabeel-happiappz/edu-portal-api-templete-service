from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    createdDate = serializers.DateTimeField(
        source='created_date', read_only=True)
    questionsAttnd = serializers.IntegerField(source='questions_attend')
    correctAnswer = serializers.IntegerField(source='correct_answer')
    percentage = serializers.FloatField(read_only=True)
    isPass = serializers.BooleanField(source='is_pass', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'username', 'createdDate',
            'questionsAttnd', 'correctAnswer',
            'percentage', 'isPass'
        ]

    def create(self, validated_data):
        # calculate
        attended = validated_data['questions_attend']
        correct = validated_data['correct_answer']
        pct = (correct / attended * 100) if attended else 0
        report = Report.objects.create(
            username=validated_data['username'],
            questions_attend=attended,
            correct_answer=correct,
            percentage=pct,
            is_pass=(pct >= 80)
        )
        return report
