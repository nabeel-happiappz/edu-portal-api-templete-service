from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'question_type', 'department', 'duration', 'created_at')
    list_filter = ('question_type', 'department')
    search_fields = ('content', 'department')
    date_hierarchy = 'created_at'
