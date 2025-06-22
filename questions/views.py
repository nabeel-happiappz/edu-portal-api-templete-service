from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing educational questions
    """
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['question_type', 'department', 'courses', 'roles']
    search_fields = ['content', 'department']
    ordering_fields = ['created_at', 'updated_at', 'duration']
    ordering = ['-created_at']

    def get_queryset(self):
        return Question.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        # Implement soft delete
        instance.is_deleted = True
        instance.save()
