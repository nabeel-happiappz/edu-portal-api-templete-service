from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, ExamViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'', ExamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/start/', ExamViewSet.as_view({'post': 'start'}), name='exam-start'),
    path('<int:pk>/questions/', ExamViewSet.as_view({'get': 'questions'}), name='exam-questions'),
    path('<int:pk>/submit/', ExamViewSet.as_view({'post': 'submit'}), name='exam-submit'),
    path('<int:pk>/results/', ExamViewSet.as_view({'get': 'results'}), name='exam-results'),
]
