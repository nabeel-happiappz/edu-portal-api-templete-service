from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer for dashboard statistics
    """
    total_courses = serializers.IntegerField(help_text="Total number of courses available")
    total_students = serializers.IntegerField(help_text="Total number of users with role 'student'")
    total_users = serializers.IntegerField(help_text="Total number of users with role 'user'")
    total_departments = serializers.IntegerField(help_text="Total number of departments available")
    total_payments = serializers.IntegerField(help_text="Total number of payments available")
    total_questions = serializers.IntegerField(help_text="Total number of questions available")


class StudentStatsSerializer(serializers.Serializer):
    """
    Serializer for student statistics
    """
    username = serializers.CharField(help_text="Username of the student")
    practice_sessions = serializers.IntegerField(help_text="Total number of practice sessions (reports)")
    questions_completed = serializers.IntegerField(help_text="Total number of questions attempted")
