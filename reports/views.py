from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.db.models import Count, Sum, Q
from .models import Report
from .serializers import ReportSerializer
from courses.models import Course
from users.models import User
from payments.models import Payment


# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    """
    list: GET /api/reports/ (optional ?username=)
    create: POST /api/reports/
    retrieve: GET /api/reports/{id}/
    destroy: DELETE /api/reports/{id}/
    """
    queryset = Report.objects.all().order_by('-created_date')
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    # ↓ disable pagination
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username')
        if username:
            qs = qs.filter(username=username)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        report_id = instance.pk
        self.perform_destroy(instance)
        return Response(
            {"message": f"Report with ID {report_id} deleted successfully"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='admin_report')
    def admin_report(self, request):
        """
        GET /api/reports/admin_report/
        Returns admin dashboard statistics
        """
        # Total courses
        total_courses = Course.objects.count()
        
        # Total students (users with role 'student')
        total_students = User.objects.filter(role='student').count()
        
        # Total users (users with role 'user')
        total_users = User.objects.filter(role='user').count()
        
# Total revenue (sum of all paid payments)
        total_revenue = Payment.objects.filter(status='Paid').aggregate(total=Sum('amount'))['total'] or 0
        
        # Course enrollment report
        # Group payments by course and count students and sum revenue (only paid payments)
        course_enrollment = Payment.objects.values('course').annotate(
            students=Count('studentName', distinct=True),
            revenue=Sum('amount', filter=Q(status='Paid'))
        ).order_by('course')
        
        # Get course names for the enrollment report
        enrollment_report = []
        for enrollment in course_enrollment:
            try:
                course = Course.objects.get(code=enrollment['course'])
                enrollment_report.append({
                    'courseName': course.name,
                    'courseCode': enrollment['course'],
                    'students': enrollment['students'],
                    'revenue': float(enrollment['revenue'] or 0)
                })
            except Course.DoesNotExist:
                # If course not found, still include it with course code as name
                enrollment_report.append({
                    'courseName': enrollment['course'],
                    'courseCode': enrollment['course'],
                    'students': enrollment['students'],
                    'revenue': float(enrollment['revenue'] or 0)
                })
        
        # Pending payments (status = 'Pending')
        pending_payments = Payment.objects.filter(status='Pending').count()
        
        # Completed payments (status = 'Paid')
        completed_payments = Payment.objects.filter(status='Paid').count()
        
        response_data = {
            'totalCourses': total_courses,
            'totalStudents': total_students,
            'totalUsers': total_users,
            'totalRevenue': float(total_revenue),
            'courseEnrollmentReport': enrollment_report,
            'pendingPayments': pending_payments,
            'completedPayments': completed_payments
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
