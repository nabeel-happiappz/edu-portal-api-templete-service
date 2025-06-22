from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, GuestProfile, IPLog, DeviceLock

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
    email = serializers.EmailField(required=True)
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
