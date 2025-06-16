from rest_framework import serializers
from users.models import User, UserProfile, GuestProfile, IPLog, DeviceLock
from exams.models import Department, Question, Answer, Exam, ExamAnswer
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta


class AdminUserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    exam_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'is_active', 'is_staff', 'date_joined', 'profile', 'exam_count')
    
    def get_profile(self, obj):
        try:
            return {
                'access_start': obj.profile.access_start,
                'access_end': obj.profile.access_end,
                'has_active_access': obj.profile.has_active_access
            }
        except UserProfile.DoesNotExist:
            return None
    
    def get_exam_count(self, obj):
        return obj.exams.count()


class AdminGuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = '__all__'


class AdminDepartmentSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'question_count')
    
    def get_question_count(self, obj):
        return obj.questions.count()


class AdminQuestionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    answer_count = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ('id', 'department', 'department_name', 'question_type', 
                 'content', 'media_url', 'created_by', 'created_by_name', 
                 'created_at', 'updated_at', 'answer_count')
    
    def get_answer_count(self, obj):
        return obj.answers.count()
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.email
        return None


class AdminAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.content', read_only=True)
    
    class Meta:
        model = Answer
        fields = ('id', 'question', 'question_text', 'text', 'is_correct')


class AdminExamSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    answer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ('id', 'user', 'user_email', 'department', 'department_name', 
                 'status', 'start_time', 'end_time', 'score', 'answer_count')
    
    def get_answer_count(self, obj):
        return obj.answers.count()


class AdminDeviceLockSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = DeviceLock
        fields = ('id', 'user', 'user_email', 'device_fingerprint', 
                 'is_locked', 'locked_reason', 'created_at', 'updated_at')


class ParticipationReportSerializer(serializers.Serializer):
    date_range = serializers.CharField(read_only=True)
    total_users = serializers.IntegerField(read_only=True)
    active_users = serializers.IntegerField(read_only=True)
    new_users = serializers.IntegerField(read_only=True)
    total_exams = serializers.IntegerField(read_only=True)
    completed_exams = serializers.IntegerField(read_only=True)
    average_score = serializers.FloatField(read_only=True)
    department_breakdown = serializers.DictField(read_only=True)


class PassRateReportSerializer(serializers.Serializer):
    date_range = serializers.CharField(read_only=True)
    total_exams = serializers.IntegerField(read_only=True)
    passing_exams = serializers.IntegerField(read_only=True)
    overall_pass_rate = serializers.FloatField(read_only=True)
    department_breakdown = serializers.DictField(read_only=True)
    question_type_breakdown = serializers.DictField(read_only=True)
