from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, StudentProfileViewSet, create_student, list_students, convert_user_to_student

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'student-profiles', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
    path('<int:pk>/remove/', UserViewSet.as_view({'delete': 'remove'}), name='user-remove'),
    path('students/list/', list_students, name='list-students'),
    path('convert-to-student/', convert_user_to_student, name='convert-user-to-student'),
]
