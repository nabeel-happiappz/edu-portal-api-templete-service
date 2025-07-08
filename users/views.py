from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import UserProfile, GuestProfile, IPLog, DeviceLock, StudentProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserWithProfileSerializer,
    RegisterSerializer, LoginSerializer, GuestProfileSerializer,
    GuestRegisterSerializer, OTPVerifySerializer, IPLogSerializer,
    DeviceLockSerializer, StudentProfileSerializer, StudentCreationSerializer,
    UserWithStudentProfileSerializer
)
from .permissions import IsOwnerOrAdmin
from .services import StudentService

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """
    Custom login view for user authentication
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data['username_or_email']
        password = serializer.validated_data['password']

        # Determine if input is email or username
        if '@' in username_or_email:
            # It's an email
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            # It's a username
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Log the successful login
        IPLog.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserWithProfileSerializer(user).data
        })
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Remove all authentication requirements
    
    def get_serializer_class(self):
        if self.action == 'me' or self.action == 'retrieve':
            return UserWithProfileSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's profile
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        """
        Explicitly delete a user and all related data
        """
        try:
            user = self.get_object()
            print(f"Deleting user with ID: {user.id}")

            # Delete related models first
            UserProfile.objects.filter(user=user).delete()
            IPLog.objects.filter(user=user).delete()
            DeviceLock.objects.filter(user=user).delete()

            # Delete the user
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Error in custom delete: {e}")
            return Response(
                {"detail": f"Failed to delete user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_destroy(self, instance):
        # Perform hard delete like in QuestionViewSet
        try:
            # Force cascade deletion of related objects
            user_id = instance.id
            # Delete related models first
            UserProfile.objects.filter(user_id=user_id).delete()
            IPLog.objects.filter(user_id=user_id).delete()
            DeviceLock.objects.filter(user_id=user_id).delete()
            # Finally delete the user
            instance.delete()
        except Exception as e:
            # Log the error and raise it to make it visible in the response
            print(f"Error deleting user: {e}")
            raise


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user profile management
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class StudentProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for student profile management
    """
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Remove all authentication requirements
    
    def get_permissions(self):
        """
        Override to ensure AllowAny for all actions
        """
        return [permissions.AllowAny()]
    
    def get_authenticators(self):
        """
        Override to remove all authenticators
        """
        return []
    
    def get_queryset(self):
        # Return all student profiles since authentication is removed
        return StudentProfile.objects.all()
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to ensure no authentication is required
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_username(self, request):
        """
        Get student profile by username
        Usage: GET /api/users/student-profiles/by_username/?username=student123
        """
        username = request.query_params.get('username')
        if not username:
            return Response(
                {"error": "Username parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
            student_profile = StudentProfile.objects.get(user=user)
            
            # No authentication required - return student profile
            serializer = self.get_serializer(student_profile)
            return Response(serializer.data)
            
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Student profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['delete'])
    def hard_delete(self, request, pk=None):
        """
        Completely delete a student and all related data from the database
        Usage: DELETE /api/users/student-profiles/{id}/hard_delete/
        """
        try:
            student_profile = self.get_object()
            user = student_profile.user
            
            # No authentication required - allow anyone to delete students
            # Delete all related data in proper order
            with transaction.atomic():
                # Delete IP logs
                IPLog.objects.filter(user=user).delete()
                
                # Delete device locks
                DeviceLock.objects.filter(user=user).delete()
                
                # Delete user profile if exists
                UserProfile.objects.filter(user=user).delete()
                
                # Delete student profile
                student_profile.delete()
                
                # Finally delete the user
                user.delete()
            
            return Response(
                {"message": "Student and all related data deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            return Response(
                {"error": f"Failed to delete student: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def list_students(request):
    """
    Simple function-based view to list all students without authentication
    """
    try:
        students = StudentProfile.objects.all()
        serializer = StudentProfileSerializer(students, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {"error": f"Failed to fetch students: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def update_password_with_old(request):
    """
    Update password using the old password and username or email
    """
    username_or_email = request.data.get('username_or_email')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not username_or_email:
        return Response({"detail": "Username or email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not old_password:
        return Response({"detail": "Old password is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not new_password:
        return Response({"detail": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Determine if input is email or username
        if '@' in username_or_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = User.objects.get(username=username_or_email)

        if not user.check_password(old_password):
            return Response({"detail": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully."})
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def update_password_with_username(request):
    """
    Update password using only the username or email
    """
    username_or_email = request.data.get('username_or_email')
    new_password = request.data.get('new_password')

    if not username_or_email:
        return Response({"detail": "Username or email is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not new_password:
        return Response({"detail": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Determine if input is email or username
        if '@' in username_or_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = User.objects.get(username=username_or_email)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully."})
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def create_student(request):
    """
    API endpoint for creating a student with both user account and student profile
    NO VALIDATION - accepts any JSON data and creates student with defaults
    
    Endpoint: POST /api/students/create
    
    This endpoint accepts any student data and creates:
    1. A User account with role='student'
    2. A StudentProfile with detailed student information
    
    Missing fields are filled with defaults. All operations are wrapped in a transaction.
    """
    
    try:
        # Use raw request data directly - no validation
        student_data = request.data if request.data else {}
        
        # Use the service layer to create the student
        user, student_profile = StudentService.create_student(student_data)
        
        # Return the created user and profile data
        user_serializer = UserWithStudentProfileSerializer(user)
        
        return Response(
            {
                "message": "Student created successfully",
                "user": user_serializer.data,
                "student_id": student_profile.id
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {
                "error": "Student creation failed",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def convert_user_to_student(request):
    """
    API endpoint for converting an existing user to a student
    
    Endpoint: POST /api/users/convert-to-student
    
    This endpoint accepts:
    - email or user_id to identify the existing user
    - student profile data to create the StudentProfile
    
    Request body example:
    {
        "email": "user@example.com",  // or "user_id": 123
        "name": "John Student",
        "address": "123 Main St",
        "district": "Central",
        "state": "California",
        "pinCode": "90001",
        "courses": ["NCLEX", "DHA"],
        "mobile": "555-123-4567",
        "countryCode": "+1",
        "mobileVerified": true,
        "emailVerified": true,
        "startDate": "2024-01-15",
        "endDate": "2024-07-15"
    }
    """
    
    try:
        # Get request data
        request_data = request.data if request.data else {}
        
        # Find the user by email or user_id
        user = None
        if request_data.get('email'):
            try:
                user = User.objects.get(email=request_data['email'])
            except User.DoesNotExist:
                return Response(
                    {
                        "error": "User not found",
                        "details": f"No user found with email: {request_data['email']}"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        elif request_data.get('user_id'):
            try:
                user = User.objects.get(id=request_data['user_id'])
            except User.DoesNotExist:
                return Response(
                    {
                        "error": "User not found",
                        "details": f"No user found with ID: {request_data['user_id']}"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "error": "Missing user identifier",
                    "details": "Please provide either 'email' or 'user_id' to identify the user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use the service layer to convert the user
        user, student_profile = StudentService.convert_user_to_student(user, request_data)
        
        # Return the updated user and profile data
        user_serializer = UserWithStudentProfileSerializer(user)
        
        return Response(
            {
                "message": "User converted to student successfully",
                "user": user_serializer.data,
                "student_id": student_profile.id
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {
                "error": "User to student conversion failed",
                "details": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
