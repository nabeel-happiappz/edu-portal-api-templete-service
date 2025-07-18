from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model with email as username field
    """
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('admin', 'Administrator'),
        ('student', 'Paid Student User'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Extended profile for paid students
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    access_start = models.DateTimeField(null=True, blank=True)
    access_end = models.DateTimeField(null=True, blank=True)
    device_fingerprint = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"
    
    @property
    def has_active_access(self):
        now = timezone.now()
        return (self.access_start is not None and 
                self.access_end is not None and 
                self.access_start <= now <= self.access_end)


class GuestProfile(models.Model):
    """
    Profile for guest demo users
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    exam_interested = models.CharField(max_length=255, blank=True)
    device_fingerprint = models.CharField(max_length=255, blank=True)
    demo_used = models.BooleanField(default=False)
    demo_questions_attempted = models.IntegerField(default=0)
    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email


class IPLog(models.Model):
    """
    Log for tracking user IP addresses and locations
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255, blank=True)
    user_agent = models.TextField(blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return f"IP Log for {self.user.email}"
        elif self.guest:
            return f"IP Log for guest {self.guest.email}"
        return f"IP Log for {self.ip_address}"


class DeviceLock(models.Model):
    """
    Model to track and manage device locks
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_fingerprint = models.CharField(max_length=255)
    is_locked = models.BooleanField(default=False)
    locked_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'device_fingerprint')
    
    def __str__(self):
        status = "Locked" if self.is_locked else "Unlocked"
        return f"{self.user.email} - {status}"


class StudentProfile(models.Model):
    """
    Detailed profile for student users with additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=255, blank=True, default='')
    address = models.TextField(blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    pin_code = models.CharField(max_length=10, blank=True, default='')
    courses = models.JSONField(default=list, help_text="List of courses student is enrolled in")
    mobile = models.CharField(max_length=20, blank=True, default='')
    country_code = models.CharField(max_length=5, default="+1", blank=True)
    mobile_verified = models.BooleanField(default=False)
    email = models.EmailField(blank=True, default='')
    email_verified = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Student Profile for {self.name} ({self.user.email})"
    
    @property
    def is_enrollment_active(self):
        """Check if student enrollment is currently active"""
        if not self.start_date or not self.end_date:
            return False
        from django.utils import timezone
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date
    
    @property
    def full_mobile(self):
        """Get full mobile number with country code"""
        return f"{self.country_code}{self.mobile}"
