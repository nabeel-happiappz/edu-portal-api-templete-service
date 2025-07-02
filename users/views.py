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
    Custom login view for user authentication
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response(
                {"detail": "No active account found with the given credentials"},
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
