from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q, F
from django.utils import timezone
from datetime import timedelta
import csv
from django.http import HttpResponse
import io
import xlsxwriter

from users.models import User, UserProfile, GuestProfile, IPLog, DeviceLock
from exams.models import Department, Question, Answer, Exam, ExamAnswer
from users.permissions import IsAdminUser
from .serializers import (
    AdminUserSerializer, AdminGuestProfileSerializer,
    AdminDepartmentSerializer, AdminQuestionSerializer,
    AdminAnswerSerializer, AdminExamSerializer,
    AdminDeviceLockSerializer, ParticipationReportSerializer,
    PassRateReportSerializer
)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing users
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def reset_device(self, request, pk=None):
        """
        Reset device fingerprint for a user
        """
        user = self.get_object()
        
        try:
            profile = user.profile
            profile.device_fingerprint = ''
            profile.save()
            
            # Reset any device locks
            DeviceLock.objects.filter(user=user).update(is_locked=False)
            
            return Response({
                "message": f"Device fingerprint reset for {user.email}"
            }, status=status.HTTP_200_OK)
            
        except UserProfile.DoesNotExist:
            return Response({
                "message": "User profile not found"
            }, status=status.HTTP_404_NOT_FOUND)


class AdminGuestProfileViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing guest profiles
    """
    queryset = GuestProfile.objects.all()
    serializer_class = AdminGuestProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def reset_demo(self, request, pk=None):
        """
        Reset demo status for a guest user
        """
        guest = self.get_object()
        guest.demo_used = False
        guest.demo_questions_attempted = 0
        guest.save()
        
        return Response({
            "message": f"Demo reset for {guest.email}"
        }, status=status.HTTP_200_OK)


class AdminDepartmentViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing departments
    """
    queryset = Department.objects.all()
    serializer_class = AdminDepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class AdminQuestionViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing questions
    """
    queryset = Question.objects.all()
    serializer_class = AdminQuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['department', 'question_type']
    search_fields = ['content']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AdminAnswerViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing answers
    """
    queryset = Answer.objects.all()
    serializer_class = AdminAnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['question', 'is_correct']


class AdminExamViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing exams
    """
    queryset = Exam.objects.all()
    serializer_class = AdminExamSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['user', 'department', 'status']


class AdminDeviceLockViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for managing device locks
    """
    queryset = DeviceLock.objects.all()
    serializer_class = AdminDeviceLockSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['user', 'is_locked']
    
    @action(detail=True, methods=['post'])
    def unlock(self, request, pk=None):
        """
        Unlock a device
        """
        device_lock = self.get_object()
        device_lock.is_locked = False
        device_lock.locked_reason = ''
        device_lock.save()
        
        return Response({
            "message": f"Device unlocked for {device_lock.user.email}"
        }, status=status.HTTP_200_OK)


class ReportViewSet(viewsets.ViewSet):
    """
    ViewSet for generating reports
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def participation(self, request):
        """
        Generate participation report
        """
        # Get date range from query params (default to last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get format from query params (default to JSON)
        report_format = request.query_params.get('format', 'json')
        
        # Gather report data
        data = {
            'date_range': f"Last {days} days",
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(last_login__gte=start_date).count(),
            'new_users': User.objects.filter(date_joined__gte=start_date).count(),
            'total_exams': Exam.objects.filter(start_time__gte=start_date).count(),
            'completed_exams': Exam.objects.filter(
                start_time__gte=start_date,
                status='completed'
            ).count(),
            'average_score': Exam.objects.filter(
                start_time__gte=start_date,
                status='completed'
            ).aggregate(avg_score=Avg('score'))['avg_score'] or 0,
        }
        
        # Get department breakdown
        department_data = Exam.objects.filter(
            start_time__gte=start_date
        ).values(
            'department__name'
        ).annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            avg_score=Avg('score', filter=Q(status='completed'))
        ).order_by('department__name')
        
        data['department_breakdown'] = {
            item['department__name']: {
                'total': item['total'],
                'completed': item['completed'],
                'avg_score': item['avg_score'] or 0
            } for item in department_data
        }
        
        # Handle different output formats
        if report_format == 'csv':
            return self._generate_csv_report(data, 'participation_report.csv')
        elif report_format == 'excel':
            return self._generate_excel_report(data, 'participation_report.xlsx')
        else:
            serializer = ParticipationReportSerializer(data)
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pass_rate(self, request):
        """
        Generate pass rate report
        """
        # Get date range from query params (default to last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get passing score from query params (default to 70)
        passing_score = float(request.query_params.get('passing_score', 70))
        
        # Get format from query params (default to JSON)
        report_format = request.query_params.get('format', 'json')
        
        # Get completed exams in the date range
        completed_exams = Exam.objects.filter(
            end_time__gte=start_date,
            status='completed'
        )
        
        total_exams = completed_exams.count()
        passing_exams = completed_exams.filter(score__gte=passing_score).count()
        
        # Calculate overall pass rate
        overall_pass_rate = (passing_exams / total_exams * 100) if total_exams > 0 else 0
        
        # Gather report data
        data = {
            'date_range': f"Last {days} days",
            'total_exams': total_exams,
            'passing_exams': passing_exams,
            'overall_pass_rate': overall_pass_rate,
        }
        
        # Get department breakdown
        department_data = completed_exams.values(
            'department__name'
        ).annotate(
            total=Count('id'),
            passing=Count('id', filter=Q(score__gte=passing_score)),
            avg_score=Avg('score')
        ).order_by('department__name')
        
        data['department_breakdown'] = {
            item['department__name']: {
                'total': item['total'],
                'passing': item['passing'],
                'pass_rate': (item['passing'] / item['total'] * 100) if item['total'] > 0 else 0,
                'avg_score': item['avg_score'] or 0
            } for item in department_data
        }
        
        # Get question type breakdown
        question_data = ExamAnswer.objects.filter(
            exam__in=completed_exams
        ).values(
            'question__question_type'
        ).annotate(
            total=Count('id'),
            correct=Count('id', filter=Q(is_correct=True))
        ).order_by('question__question_type')
        
        data['question_type_breakdown'] = {
            dict(Question.QUESTION_TYPES).get(item['question__question_type'], 'Unknown'): {
                'total': item['total'],
                'correct': item['correct'],
                'success_rate': (item['correct'] / item['total'] * 100) if item['total'] > 0 else 0
            } for item in question_data
        }
        
        # Handle different output formats
        if report_format == 'csv':
            return self._generate_csv_report(data, 'pass_rate_report.csv')
        elif report_format == 'excel':
            return self._generate_excel_report(data, 'pass_rate_report.xlsx')
        else:
            serializer = PassRateReportSerializer(data)
            return Response(serializer.data)
    
    def _generate_csv_report(self, data, filename):
        """
        Generate a CSV report from the data
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['Report Type', 'Date Range'])
        writer.writerow([filename.replace('.csv', ''), data['date_range']])
        writer.writerow([])
        
        # Write summary data
        for key, value in data.items():
            if key not in ['date_range', 'department_breakdown', 'question_type_breakdown']:
                writer.writerow([key.replace('_', ' ').title(), value])
        
        writer.writerow([])
        
        # Write department breakdown
        if 'department_breakdown' in data:
            writer.writerow(['Department Breakdown'])
            writer.writerow(['Department', 'Total', 'Completed/Passing', 'Average Score/Pass Rate'])
            
            for dept, dept_data in data['department_breakdown'].items():
                if 'completed' in dept_data:  # Participation report
                    writer.writerow([
                        dept, 
                        dept_data['total'], 
                        dept_data['completed'],
                        f"{dept_data['avg_score']:.2f}%"
                    ])
                else:  # Pass rate report
                    writer.writerow([
                        dept, 
                        dept_data['total'], 
                        dept_data['passing'],
                        f"{dept_data['pass_rate']:.2f}%"
                    ])
        
        writer.writerow([])
        
        # Write question type breakdown
        if 'question_type_breakdown' in data:
            writer.writerow(['Question Type Breakdown'])
            writer.writerow(['Question Type', 'Total', 'Correct', 'Success Rate'])
            
            for q_type, q_data in data['question_type_breakdown'].items():
                writer.writerow([
                    q_type, 
                    q_data['total'], 
                    q_data['correct'],
                    f"{q_data['success_rate']:.2f}%"
                ])
        
        return response
    
    def _generate_excel_report(self, data, filename):
        """
        Generate an Excel report from the data
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Report')
        
        # Formats
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        subheader_format = workbook.add_format({
            'bold': True,
            'font_size': 11,
            'bg_color': '#D9E1F2',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1
        })
        
        percent_format = workbook.add_format({
            'border': 1,
            'num_format': '0.00%'
        })
        
        # Write title
        report_title = filename.replace('.xlsx', '').replace('_', ' ').title()
        worksheet.write(0, 0, report_title, header_format)
        worksheet.write(0, 1, data['date_range'], header_format)
        
        # Write summary data
        row = 2
        worksheet.write(row, 0, 'Summary', subheader_format)
        worksheet.write(row, 1, '', subheader_format)
        row += 1
        
        for key, value in data.items():
            if key not in ['date_range', 'department_breakdown', 'question_type_breakdown']:
                worksheet.write(row, 0, key.replace('_', ' ').title(), cell_format)
                
                # Format percentages
                if 'rate' in key or 'average' in key:
                    worksheet.write(row, 1, value / 100, percent_format)
                else:
                    worksheet.write(row, 1, value, cell_format)
                    
                row += 1
        
        row += 1
        
        # Write department breakdown
        if 'department_breakdown' in data:
            worksheet.write(row, 0, 'Department Breakdown', subheader_format)
            worksheet.merge_range(row, 1, row, 3, '', subheader_format)
            row += 1
            
            if 'completed' in next(iter(data['department_breakdown'].values())):  # Participation report
                worksheet.write(row, 0, 'Department', subheader_format)
                worksheet.write(row, 1, 'Total', subheader_format)
                worksheet.write(row, 2, 'Completed', subheader_format)
                worksheet.write(row, 3, 'Average Score', subheader_format)
                row += 1
                
                for dept, dept_data in data['department_breakdown'].items():
                    worksheet.write(row, 0, dept, cell_format)
                    worksheet.write(row, 1, dept_data['total'], cell_format)
                    worksheet.write(row, 2, dept_data['completed'], cell_format)
                    worksheet.write(row, 3, dept_data['avg_score'] / 100, percent_format)
                    row += 1
            else:  # Pass rate report
                worksheet.write(row, 0, 'Department', subheader_format)
                worksheet.write(row, 1, 'Total', subheader_format)
                worksheet.write(row, 2, 'Passing', subheader_format)
                worksheet.write(row, 3, 'Pass Rate', subheader_format)
                row += 1
                
                for dept, dept_data in data['department_breakdown'].items():
                    worksheet.write(row, 0, dept, cell_format)
                    worksheet.write(row, 1, dept_data['total'], cell_format)
                    worksheet.write(row, 2, dept_data['passing'], cell_format)
                    worksheet.write(row, 3, dept_data['pass_rate'] / 100, percent_format)
                    row += 1
        
        row += 1
        
        # Write question type breakdown
        if 'question_type_breakdown' in data:
            worksheet.write(row, 0, 'Question Type Breakdown', subheader_format)
            worksheet.merge_range(row, 1, row, 3, '', subheader_format)
            row += 1
            
            worksheet.write(row, 0, 'Question Type', subheader_format)
            worksheet.write(row, 1, 'Total', subheader_format)
            worksheet.write(row, 2, 'Correct', subheader_format)
            worksheet.write(row, 3, 'Success Rate', subheader_format)
            row += 1
            
            for q_type, q_data in data['question_type_breakdown'].items():
                worksheet.write(row, 0, q_type, cell_format)
                worksheet.write(row, 1, q_data['total'], cell_format)
                worksheet.write(row, 2, q_data['correct'], cell_format)
                worksheet.write(row, 3, q_data['success_rate'] / 100, percent_format)
                row += 1
        
        # Adjust column widths
        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, 3, 15)
        
        workbook.close()
        
        # Create the response
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
