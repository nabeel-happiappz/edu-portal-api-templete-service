from django.contrib import admin
from .models import Department, Question, Answer, Exam, ExamAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'question_type', 'content', 'created_at')
    list_filter = ('department', 'question_type', 'created_at')
    search_fields = ('content',)
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


class ExamAnswerInline(admin.TabularInline):
    model = ExamAnswer
    extra = 0
    readonly_fields = ('question', 'selected_answer', 'is_correct', 'answered_at')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'status', 'start_time', 'end_time', 'score')
    list_filter = ('status', 'department', 'start_time')
    search_fields = ('user__email', 'department__name')
    inlines = [ExamAnswerInline]


@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'question', 'is_correct', 'answered_at')
    list_filter = ('is_correct', 'answered_at')
    search_fields = ('exam__user__email', 'question__content')
