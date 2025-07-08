from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import User
from courses.models import Course
from departments.models import Department
from payments.models import Payment
from questions.models import Question
from .serializers import DashboardStatsSerializer


@swagger_auto_schema(
    method='get',
    operation_description="Get dashboard statistics for admin panel",
    operation_summary="Admin Dashboard Statistics",
    responses={
        200: openapi.Response(
            description="Dashboard statistics retrieved successfully",
            schema=DashboardStatsSerializer
        )
    },
    tags=['Dashboard']
)
@api_view(['GET'])
@permission_classes([AllowAny])
def admin_dashboard_stats(request):
    """
    Get dashboard statistics for admin panel.
    No authentication required.
    
    Returns:
    - total_courses: Total number of courses available
    - total_students: Total number of users with role 'student'
    - total_users: Total number of users with role 'user'
    - total_departments: Total number of departments available
    - total_payments: Total number of payments available
    - total_questions: Total number of active questions available
    """
    # Get statistics
    stats = {
        'total_courses': Course.objects.count(),
        'total_students': User.objects.filter(role='student').count(),
        'total_users': User.objects.filter(role='user').count(),
        'total_departments': Department.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_questions': Question.objects.filter(is_deleted=False).count()
    }
    
    serializer = DashboardStatsSerializer(data=stats)
    serializer.is_valid()
    
    return Response(serializer.data, status=status.HTTP_200_OK)
