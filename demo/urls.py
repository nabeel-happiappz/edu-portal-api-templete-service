from django.urls import path
from .views import DemoViewSet

urlpatterns = [
    path('register/', DemoViewSet.as_view({'post': 'register'}), name='demo-register'),
    path('verify-otp/', DemoViewSet.as_view({'post': 'verify_otp'}), name='demo-verify-otp'),
    path('questions/', DemoViewSet.as_view({'get': 'questions'}), name='demo-questions'),
    path('submit/', DemoViewSet.as_view({'post': 'submit'}), name='demo-submit'),
]
