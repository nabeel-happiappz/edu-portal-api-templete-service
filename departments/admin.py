from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
