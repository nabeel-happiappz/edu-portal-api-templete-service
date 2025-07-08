from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard_stats, name='admin-dashboard-stats'),
    path('student/', views.student_dashboard_stats, name='student-dashboard-stats'),
]
