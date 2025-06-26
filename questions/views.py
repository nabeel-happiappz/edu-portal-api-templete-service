import os
from django.http import Http404, FileResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, filters as drf_filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as df_filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings

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
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend,
                       drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = QuestionFilter
    search_fields = ['content', 'department']

    @action(detail=False, methods=['get'], url_path='user')
    def user_questions(self, request):
        """
        Returns all questions that have 'user' in their roles field
        """
        queryset = Question.objects.filter(roles__contains=['user'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='student')
    def student_questions(self, request):
        """
        Returns all questions that have 'student' in their roles field
        """
        queryset = Question.objects.filter(roles__contains=['student'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    ordering_fields = ['created_at', 'updated_at', 'duration']
    ordering = ['-created_at']

    def get_queryset(self):
        return Question.objects.all()

    def perform_destroy(self, instance):
        # Perform hard delete
        instance.delete()


class QuestionImageUploadView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        # 1. Validate question exists
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404("Question not found")

        # 2. Validate payload
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'detail': 'No image file provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 3. Build storage path
        ext = os.path.splitext(image_file.name)[1]  # keep original extension
        filename = f"{pk}_image{ext}"
        save_dir = os.path.join(settings.MEDIA_ROOT, 'questions', 'images')
        os.makedirs(save_dir, exist_ok=True)
        full_path = os.path.join(save_dir, filename)

        # 4. Write file
        with open(full_path, 'wb+') as dest:
            for chunk in image_file.chunks():
                dest.write(chunk)

        # 5. Respond with success and URL
        url = request.build_absolute_uri(
            settings.MEDIA_URL + f"questions/images/{filename}"
        )
        return Response({'image_url': url}, status=status.HTTP_201_CREATED)


class QuestionImageFetchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        # 1. Ensure question exists
        if not Question.objects.filter(pk=pk).exists():
            raise Http404("Question not found")

        # 2. Compute file path (we’ll search for any file starting with `<pk>_image.`)
        dir_path = os.path.join(settings.MEDIA_ROOT, 'questions', 'images')
        if not os.path.isdir(dir_path):
            raise Http404("No images uploaded yet")

        # Find matching file
        for fname in os.listdir(dir_path):
            if fname.startswith(f"{pk}_image"):
                return FileResponse(open(os.path.join(dir_path, fname), 'rb'),
                                    content_type='image/*')
        raise Http404("Image not found")
