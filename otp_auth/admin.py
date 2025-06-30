from django.contrib import admin
from .models import OTP

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'otp_type', 'code', 'is_verified', 'created_at', 'expires_at')
    search_fields = ('identifier', 'code')
    list_filter = ('otp_type', 'is_verified', 'created_at', 'expires_at')
