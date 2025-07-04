from django.urls import path
from . import views

urlpatterns = [
    # List all active packages and create new package
    path('packages/', views.list_create_packages, name='list-create-packages'),
    # Get, update, delete specific package
    path('packages/<int:package_id>/', views.package_detail, name='package-detail'),
]
