from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionTypeViewSet

router = DefaultRouter()
router.register('question-types', QuestionTypeViewSet, basename='question-types')

urlpatterns = [
    path('', include(router.urls)),
]
