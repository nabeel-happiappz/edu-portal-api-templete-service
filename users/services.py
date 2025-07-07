from django.db import transaction
from django.contrib.auth import get_user_model
from .models import StudentProfile
from .serializers import RegisterSerializer
from datetime import datetime

User = get_user_model()


class StudentService:
    """
    Service class for handling student-related operations
    """
    
    @staticmethod
    @transaction.atomic
    def create_student(student_data):
        """
        Create a student with user account and student profile in a single transaction
        NO VALIDATION - accepts any data and creates with defaults for missing fields
        
        Args:
            student_data (dict): Dictionary containing student data
            
        Returns:
            tuple: (user, student_profile) on success
            
        Raises:
            Exception: If creation fails
        """
        try:
            import uuid
            from datetime import date
            
            # Generate defaults for missing user data
            email = student_data.get('email') or f"student_{uuid.uuid4().hex[:8]}@example.com"
            username = student_data.get('username') or f"student_{uuid.uuid4().hex[:8]}"
            password = student_data.get('password') or 'defaultpassword123'
            
            user_data = {
                'email': email,
                'username': username,
                'password': password,
                'role': 'student'  # Force role to be student
            }
            
            # Create user with minimal validation bypass
            user = User.objects.create_user(
                email=user_data['email'],
                username=user_data['username'],
                password=user_data['password']
            )
            user.role = 'student'
            user.save()
            
            # Prepare profile data with defaults for missing fields
            profile_data = {
                'name': student_data.get('name') or 'Unknown Student',
                'address': student_data.get('address') or '',
                'district': student_data.get('district') or '',
                'state': student_data.get('state') or '',
                'pin_code': student_data.get('pinCode') or '',
                'courses': student_data.get('courses') or [],
                'mobile': student_data.get('mobile') or '',
                'country_code': student_data.get('countryCode') or '+1',
                'mobile_verified': student_data.get('mobileVerified', False),
                'email': email,  # Use the same email as user
                'email_verified': student_data.get('emailVerified', False),
                'start_date': None,
                'end_date': None
            }
            
            # Handle date fields with defaults
            if student_data.get('startDate'):
                try:
                    if isinstance(student_data['startDate'], str):
                        profile_data['start_date'] = datetime.strptime(student_data['startDate'], '%Y-%m-%d').date()
                    else:
                        profile_data['start_date'] = student_data['startDate']
                except:
                    profile_data['start_date'] = date.today()
            else:
                profile_data['start_date'] = date.today()
            
            if student_data.get('endDate'):
                try:
                    if isinstance(student_data['endDate'], str):
                        profile_data['end_date'] = datetime.strptime(student_data['endDate'], '%Y-%m-%d').date()
                    else:
                        profile_data['end_date'] = student_data['endDate']
                except:
                    from datetime import timedelta
                    profile_data['end_date'] = date.today() + timedelta(days=365)
            else:
                from datetime import timedelta
                profile_data['end_date'] = date.today() + timedelta(days=365)
            
            # Create student profile without validation
            student_profile = StudentProfile.objects.create(
                user=user,
                **profile_data
            )
            
            return user, student_profile
            
        except Exception as e:
            # Transaction will automatically rollback due to @transaction.atomic decorator
            raise Exception(f"Student creation failed: {str(e)}")
    
    @staticmethod
    def get_student_by_user(user):
        """
        Get student profile for a given user
        
        Args:
            user: User instance
            
        Returns:
            StudentProfile or None
        """
        try:
            return StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            return None
    
    @staticmethod
    def get_student_by_email(email):
        """
        Get student profile by email
        
        Args:
            email (str): Student's email address
            
        Returns:
            StudentProfile or None
        """
        try:
            user = User.objects.get(email=email)
            return StudentProfile.objects.get(user=user)
        except (User.DoesNotExist, StudentProfile.DoesNotExist):
            return None
    
    @staticmethod
    def update_student_profile(student_profile, profile_data):
        """
        Update student profile with new data
        
        Args:
            student_profile: StudentProfile instance
            profile_data (dict): Dictionary containing profile data to update
            
        Returns:
            StudentProfile: Updated student profile
        """
        for field, value in profile_data.items():
            if hasattr(student_profile, field):
                setattr(student_profile, field, value)
        
        student_profile.save()
        return student_profile
