from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, GuestProfile, IPLog, DeviceLock, StudentProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'demo_used', 'demo_questions_attempted', 'otp_verified', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('demo_used', 'otp_verified')


@admin.register(IPLog)
class IPLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'guest', 'ip_address', 'location', 'login_time')
    search_fields = ('user__email', 'guest__email', 'ip_address', 'location')
    list_filter = ('login_time',)


@admin.register(DeviceLock)
class DeviceLockAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_fingerprint', 'is_locked', 'locked_reason', 'created_at', 'updated_at')
    search_fields = ('user__email', 'device_fingerprint', 'locked_reason')
    list_filter = ('is_locked', 'created_at', 'updated_at')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'email', 'mobile', 'district', 'state', 'start_date', 'end_date', 'is_enrollment_active')
    search_fields = ('name', 'user__email', 'email', 'mobile', 'district', 'state')
    list_filter = ('state', 'district', 'mobile_verified', 'email_verified', 'start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at', 'is_enrollment_active', 'full_mobile')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'email', 'email_verified')
        }),
        ('Contact Information', {
            'fields': ('mobile', 'country_code', 'mobile_verified', 'address', 'district', 'state', 'pin_code')
        }),
        ('Course Information', {
            'fields': ('courses', 'start_date', 'end_date')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'is_enrollment_active', 'full_mobile'),
            'classes': ('collapse',)
        })
    )


admin.site.register(User, CustomUserAdmin)
