from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'studentName', 'course', 'amount', 'date', 'status', 'createdAt', 'updatedAt']
    list_filter = ['status', 'course', 'date', 'createdAt']
    search_fields = ['studentName', 'course', 'status']
    ordering = ['-createdAt']
    readonly_fields = ['id', 'createdAt', 'updatedAt']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('studentName', 'course', 'amount', 'date', 'status')
        }),
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        })
    )
