from django.contrib import admin
from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'currency', 'question_count', 'validity_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'currency', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
