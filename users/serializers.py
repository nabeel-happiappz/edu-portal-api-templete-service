from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, GuestProfile, IPLog, DeviceLock, StudentProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'role')
        read_only_fields = ('id', 'is_active')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'access_start', 'access_end', 'device_fingerprint', 
                 'phone', 'address', 'has_active_access')
        read_only_fields = ('id', 'has_active_access')


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'is_active', 'role', 'profile')
        read_only_fields = ('id', 'is_active')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if 'role' in attrs and attrs['role'] not in ('user', 'admin', 'student'):
            raise serializers.ValidationError({"role": "Role must be one of: user, admin, student"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = ('id', 'name', 'email', 'phone', 'address', 'exam_interested', 
                 'device_fingerprint', 'demo_used', 'demo_questions_attempted')
        read_only_fields = ('id', 'demo_used', 'demo_questions_attempted')


class GuestRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = ('name', 'email', 'phone', 'address', 'exam_interested', 
                 'device_fingerprint')


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6, min_length=6)


class IPLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPLog
        fields = '__all__'


class DeviceLockSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = DeviceLock
        fields = ('id', 'user', 'user_email', 'device_fingerprint', 
                 'is_locked', 'locked_reason', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class StudentProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_enrollment_active = serializers.BooleanField(read_only=True)
    full_mobile = serializers.CharField(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'user_email', 'user_username', 'name', 'address', 'district', 
                 'state', 'pin_code', 'courses', 'mobile', 'country_code', 
                 'mobile_verified', 'email', 'email_verified', 'start_date', 
                 'end_date', 'is_enrollment_active', 'full_mobile', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_enrollment_active', 'full_mobile', 'user_username')


class StudentCreationSerializer(serializers.Serializer):
    """Serializer for creating a student with both user and profile data - NO VALIDATION"""
    
    # User fields
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    # Student profile fields
    name = serializers.CharField(required=False, max_length=255, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, max_length=100, allow_blank=True)
    state = serializers.CharField(required=False, max_length=100, allow_blank=True)
    pinCode = serializers.CharField(required=False, max_length=10, allow_blank=True)
    courses = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list,
        allow_empty=True
    )
    mobile = serializers.CharField(required=False, max_length=20, allow_blank=True)
    countryCode = serializers.CharField(required=False, max_length=5, default="+1", allow_blank=True)
    mobileVerified = serializers.BooleanField(required=False, default=False)
    emailVerified = serializers.BooleanField(required=False, default=False)
    startDate = serializers.DateField(required=False, format="%Y-%m-%d", allow_null=True)
    endDate = serializers.DateField(required=False, format="%Y-%m-%d", allow_null=True)


class UserWithStudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for user with student profile information"""
    student_profile = StudentProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                 'is_active', 'role', 'student_profile')
        read_only_fields = ('id', 'is_active')
