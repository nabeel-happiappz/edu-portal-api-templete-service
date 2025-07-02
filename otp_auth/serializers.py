from rest_framework import serializers
from .models import OTP

class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=255)
    otp_type = serializers.ChoiceField(choices=OTP.OTP_TYPE_CHOICES)

class OTPVerifySerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=255)
    otp_type = serializers.ChoiceField(choices=OTP.OTP_TYPE_CHOICES)
    code = serializers.CharField(max_length=6, min_length=6) 