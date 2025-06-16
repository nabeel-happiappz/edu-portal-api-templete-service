from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import UserProfile, GuestProfile, IPLog, DeviceLock
from .serializers import (
    UserSerializer, UserProfileSerializer, UserWithProfileSerializer,
    RegisterSerializer, LoginSerializer, GuestProfileSerializer,
    GuestRegisterSerializer, OTPVerifySerializer, IPLogSerializer,
    DeviceLockSerializer
)
from .permissions import IsOwnerOrAdmin

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
    Custom login view that checks device fingerprint
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        device_fingerprint = serializer.validated_data['device_fingerprint']
        
        user = get_object_or_404(User, email=email)
        
        if not user.check_password(password):
            return Response(
                {"detail": "No active account found with the given credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check if user has a profile with device fingerprint
        try:
            profile = user.profile
            
            # If user already has a device fingerprint, verify it matches
            if profile.device_fingerprint and profile.device_fingerprint != device_fingerprint:
                # Log the attempt
                IPLog.objects.create(
                    user=user,
                    ip_address=self.get_client_ip(request),
                    location=request.data.get('location', ''),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                # Check if a device lock already exists
                device_lock, created = DeviceLock.objects.get_or_create(
                    user=user,
                    device_fingerprint=profile.device_fingerprint,
                    defaults={'is_locked': False}
                )
                
                # Lock the device
                device_lock.is_locked = True
                device_lock.locked_reason = "Login attempt from unrecognized device"
                device_lock.save()
                
                return Response(
                    {"detail": "Login attempt from an unauthorized device. Please contact support."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # If this is the first login, save the device fingerprint
            if not profile.device_fingerprint:
                profile.device_fingerprint = device_fingerprint
                profile.save()
                
        except UserProfile.DoesNotExist:
            pass
        
        # Log the successful login
        IPLog.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            location=request.data.get('location', ''),
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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
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
