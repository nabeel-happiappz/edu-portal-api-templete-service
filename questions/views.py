from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as df_filters
from rest_framework.permissions import AllowAny

from .models import Question
from .serializers import QuestionSerializer


class QuestionFilter(df_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['question_type', 'department']
        # Exclude JSONFields: 'courses', 'roles', 'options', 'correct_answer'



class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing educational questions
    """
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = QuestionFilter
    search_fields = ['content', 'department']
    ordering_fields = ['created_at', 'updated_at', 'duration']
    ordering = ['-created_at']

    def get_queryset(self):
        return Question.objects.all()

    def perform_destroy(self, instance):
        # Perform hard delete
        instance.delete()
