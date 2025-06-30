from django.db import models
from django.utils import timezone

class OTP(models.Model):
    EMAIL = 'email'
    PHONE = 'phone'
    OTP_TYPE_CHOICES = [
        (EMAIL, 'Email'),
        (PHONE, 'Phone'),
    ]

    identifier = models.CharField(max_length=255)  # email or phone
    otp_type = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES, default=EMAIL)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'otp_type']),
        ]
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.identifier} ({self.otp_type}) - {self.code}"
