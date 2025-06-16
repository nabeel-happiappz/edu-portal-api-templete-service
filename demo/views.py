from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import GuestProfile, IPLog
from users.serializers import GuestRegisterSerializer, OTPVerifySerializer
from .models import DemoSession, DemoAnswer
from .serializers import (
    DemoSessionSerializer, DemoAnswerSerializer, 
    DemoQuestionListSerializer, DemoSubmitSerializer
)
import random
import string


class DemoViewSet(viewsets.ViewSet):
    """
    ViewSet for guest demo functionality
    """
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new guest user for demo access
        """
        serializer = GuestRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Create the guest profile
            guest = GuestProfile.objects.create(
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email'],
                phone=serializer.validated_data.get('phone', ''),
                address=serializer.validated_data.get('address', ''),
                exam_interested=serializer.validated_data.get('exam_interested', ''),
                device_fingerprint=serializer.validated_data.get('device_fingerprint', ''),
                otp=self.generate_otp(),
                otp_verified=False
            )
            
            # Log IP
            IPLog.objects.create(
                guest=guest,
                ip_address=self.get_client_ip(request),
                location=request.data.get('location', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send OTP (in a real system, this would be sent via email/SMS)
            self.send_otp(guest)
            
            return Response({
                "message": "Guest registered successfully. Please verify OTP.",
                "email": guest.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        """
        Verify OTP for guest user
        """
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                guest = GuestProfile.objects.get(email=email)
                
                if guest.otp_verified:
                    return Response({
                        "message": "OTP already verified."
                    }, status=status.HTTP_200_OK)
                
                if guest.otp == otp:
                    guest.otp_verified = True
                    guest.save()
                    
                    # Create a demo session
                    session = DemoSession.objects.create(guest=guest)
                    
                    return Response({
                        "message": "OTP verified successfully.",
                        "session_id": session.id
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Invalid OTP."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            except GuestProfile.DoesNotExist:
                return Response({
                    "message": "Guest not found."
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def questions(self, request):
        """
        Get demo questions for a verified guest
        """
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({
                "message": "Session ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = DemoSession.objects.get(id=session_id)
            guest = session.guest
            
            if not guest.otp_verified:
                return Response({
                    "message": "OTP not verified."
                }, status=status.HTTP_403_FORBIDDEN)
            
            if guest.demo_used:
                return Response({
                    "message": "Demo already used."
                }, status=status.HTTP_403_FORBIDDEN)
            
            serializer = DemoQuestionListSerializer(session)
            return Response(serializer.data)
            
        except DemoSession.DoesNotExist:
            return Response({
                "message": "Session not found."
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def submit(self, request):
        """
        Submit answers for demo questions
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({
                "message": "Session ID is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session = DemoSession.objects.get(id=session_id)
            guest = session.guest
            
            if not guest.otp_verified:
                return Response({
                    "message": "OTP not verified."
                }, status=status.HTTP_403_FORBIDDEN)
            
            if guest.demo_used:
                return Response({
                    "message": "Demo already used."
                }, status=status.HTTP_403_FORBIDDEN)
            
            serializer = DemoSubmitSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(session=session)
                
                # Get results
                total_questions = DemoAnswer.objects.filter(session=session).count()
                correct_answers = DemoAnswer.objects.filter(session=session, is_correct=True).count()
                
                return Response({
                    "message": "Demo completed successfully.",
                    "total_questions": total_questions,
                    "correct_answers": correct_answers,
                    "score_percentage": round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except DemoSession.DoesNotExist:
            return Response({
                "message": "Session not found."
            }, status=status.HTTP_404_NOT_FOUND)
    
    def generate_otp(self):
        """
        Generate a 6-digit OTP
        """
        return ''.join(random.choices(string.digits, k=6))
    
    def send_otp(self, guest):
        """
        Placeholder for sending OTP via email/SMS
        In a real system, this would integrate with an email/SMS service
        """
        print(f"OTP for {guest.email}: {guest.otp}")
        # In a real implementation, this would be:
        # 1. A Celery task to send the OTP
        # 2. Integration with an email or SMS service
    
    def get_client_ip(self, request):
        """
        Get client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
