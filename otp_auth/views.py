from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.mail import send_mail
from .models import OTP
from .serializers import OTPRequestSerializer, OTPVerifySerializer
import random
from datetime import timedelta

OTP_EXPIRY_MINUTES = 10
MAX_ATTEMPTS = 5

class OTPRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']
        otp_type = serializer.validated_data['otp_type']

        # Rate limiting: check for recent unexpired OTPs
        now = timezone.now()
        recent_otp = OTP.objects.filter(
            identifier=identifier,
            otp_type=otp_type,
            is_verified=False,
            expires_at__gt=now
        ).order_by('-created_at').first()
        if recent_otp:
            return Response({'detail': 'OTP already sent. Please wait before requesting again.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Generate OTP
        code = f"{random.randint(100000, 999999)}"
        expires_at = now + timedelta(minutes=OTP_EXPIRY_MINUTES)
        otp = OTP.objects.create(
            identifier=identifier,
            otp_type=otp_type,
            code=code,
            expires_at=expires_at
        )

        # Send OTP (email only for now)
        if otp_type == OTP.EMAIL:
            try:
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP code is {code}. It will expire in {OTP_EXPIRY_MINUTES} minutes.',
                    from_email=None,  # Use DEFAULT_FROM_EMAIL
                    recipient_list=[identifier],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error
                print(f"Email sending error: {str(e)}")
                # Delete the created OTP to avoid inconsistent state
                otp.delete()
                return Response({'detail': f'Failed to send OTP email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # For phone, integrate SMS provider in the future

        return Response({'detail': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']
        otp_type = serializer.validated_data['otp_type']
        code = serializer.validated_data['code']

        now = timezone.now()
        otp = OTP.objects.filter(
            identifier=identifier,
            otp_type=otp_type,
            is_verified=False,
            expires_at__gt=now
        ).order_by('-created_at').first()

        if not otp:
            return Response({'detail': 'OTP not found or expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.attempts >= MAX_ATTEMPTS:
            return Response({'detail': 'Maximum verification attempts exceeded.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        if otp.code != code:
            otp.attempts += 1
            otp.save()
            return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_verified = True
        otp.save()
        return Response({'detail': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
