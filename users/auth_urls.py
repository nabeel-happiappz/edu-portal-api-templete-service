from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, update_password_with_old, update_password_with_username

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-password-with-old/', update_password_with_old, name='update-password-with-old'),
    path('update-password/', update_password_with_username, name='update-password'),
]
