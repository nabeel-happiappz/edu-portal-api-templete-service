from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Report
from .serializers import ReportSerializer


# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    """
    list: GET /api/reports/ (optional ?username=)
    create: POST /api/reports/
    retrieve: GET /api/reports/{id}/
    destroy: DELETE /api/reports/{id}/
    """
    queryset = Report.objects.all().order_by('-created_date')
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    # ↓ disable pagination
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username')
        if username:
            qs = qs.filter(username=username)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        report_id = instance.pk
        self.perform_destroy(instance)
        return Response(
            {"message": f"Report with ID {report_id} deleted successfully"},
            status=status.HTTP_200_OK
        )
