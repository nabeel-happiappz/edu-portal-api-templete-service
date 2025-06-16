from django.contrib import admin
from .models import DemoSession, DemoAnswer


@admin.register(DemoSession)
class DemoSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'start_time', 'end_time', 'is_completed')
    list_filter = ('is_completed', 'start_time')
    search_fields = ('guest__email', 'guest__name')


@admin.register(DemoAnswer)
class DemoAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'question', 'is_correct', 'answered_at')
    list_filter = ('is_correct', 'answered_at')
    search_fields = ('session__guest__email', 'question__content')
