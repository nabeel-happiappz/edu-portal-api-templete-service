from rest_framework import serializers
from .models import Department, Question, Answer, Exam, ExamAnswer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct')
        read_only_fields = ('id',)
        extra_kwargs = {
            'is_correct': {'write_only': True}
        }


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    
    class Meta:
        model = Question
        fields = ('id', 'department', 'department_name', 'question_type', 
                 'question_type_display', 'content', 'media_url', 'answers', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExamAnswerSerializer(serializers.ModelSerializer):
    question_content = serializers.CharField(source='question.content', read_only=True)
    answer_text = serializers.CharField(source='selected_answer.text', read_only=True)
    
    class Meta:
        model = ExamAnswer
        fields = ('id', 'question', 'question_content', 'selected_answer', 
                 'answer_text', 'is_correct', 'answered_at')
        read_only_fields = ('id', 'is_correct', 'answered_at')


class ExamSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Exam
        fields = ('id', 'user', 'department', 'department_name', 'status', 
                 'start_time', 'end_time', 'score')
        read_only_fields = ('id', 'user', 'start_time', 'end_time', 'score')


class ExamDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    answers = ExamAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = ('id', 'user', 'department', 'department_name', 'status', 
                 'start_time', 'end_time', 'score', 'answers')
        read_only_fields = ('id', 'user', 'start_time', 'end_time', 'score')


class ExamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('department',)


class ExamSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            allow_empty=False
        ),
        required=True
    )
    
    def validate_answers(self, value):
        for answer_data in value:
            if 'question_id' not in answer_data or 'answer_id' not in answer_data:
                raise serializers.ValidationError(
                    "Each answer must contain 'question_id' and 'answer_id'"
                )
        return value


class ExamResultsSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    total_questions = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ('id', 'department', 'department_name', 'status', 
                 'start_time', 'end_time', 'score', 'total_questions', 
                 'correct_answers')
        read_only_fields = fields
    
    def get_total_questions(self, obj):
        return obj.answers.count()
    
    def get_correct_answers(self, obj):
        return obj.answers.filter(is_correct=True).count()
