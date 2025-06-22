from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import QuestionType
from .serializers import QuestionTypeSerializer


class QuestionTypeViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionTypeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Exclude soft-deleted question types for list view
        return QuestionType.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        # Implement soft delete
        instance.is_deleted = True
        instance.save()
