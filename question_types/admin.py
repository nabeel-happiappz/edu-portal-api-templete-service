from django.contrib import admin
from .models import QuestionType


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('is_deleted',)
    search_fields = ('code', 'name', 'description')
    ordering = ('code',)
