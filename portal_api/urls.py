"""
URL configuration for portal_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import create_student, convert_user_to_student

schema_view = get_schema_view(
    openapi.Info(
        title="David Academy Portal API",
        default_version='v1',
        description="API for online nursing exam practice system",
        contact=openapi.Contact(email="contact@davidacademy.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('users.auth_urls')),
    path('api/users/', include('users.urls')),
    path('api/demo/', include('demo.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/admin/', include('adminpanel.urls')),
    path('api/', include('question_types.urls')),
    path('api/otp/', include('otp_auth.urls')),
    path('api/questions/', include('questions.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/', include('packages.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    
    # Student creation endpoint
    path('api/students/create', create_student, name='create-student'),
    
    # User to student conversion endpoint
    path('api/users/convert-to-student', convert_user_to_student, name='convert-user-to-student'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
