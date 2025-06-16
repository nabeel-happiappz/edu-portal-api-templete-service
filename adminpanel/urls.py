from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet, AdminGuestProfileViewSet, AdminDepartmentViewSet,
    AdminQuestionViewSet, AdminAnswerViewSet, AdminExamViewSet,
    AdminDeviceLockViewSet, ReportViewSet
)

router = DefaultRouter()
router.register(r'users', AdminUserViewSet)
router.register(r'guests', AdminGuestProfileViewSet)
router.register(r'departments', AdminDepartmentViewSet)
router.register(r'questions', AdminQuestionViewSet)
router.register(r'answers', AdminAnswerViewSet)
router.register(r'exams', AdminExamViewSet)
router.register(r'device-locks', AdminDeviceLockViewSet)
router.register(r'reports', ReportViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/reset-device/', AdminUserViewSet.as_view({'post': 'reset_device'}), name='admin-reset-device'),
    path('guests/<int:pk>/reset-demo/', AdminGuestProfileViewSet.as_view({'post': 'reset_demo'}), name='admin-reset-demo'),
    path('device-locks/<int:pk>/unlock/', AdminDeviceLockViewSet.as_view({'post': 'unlock'}), name='admin-unlock-device'),
    path('reports/participation/', ReportViewSet.as_view({'get': 'participation'}), name='admin-participation-report'),
    path('reports/pass-rate/', ReportViewSet.as_view({'get': 'pass_rate'}), name='admin-pass-rate-report'),
]
