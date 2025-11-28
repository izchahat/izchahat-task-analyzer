from django.urls import path
from .views import AnalyzeTasksAPIView

urlpatterns = [
    path('analyze/', AnalyzeTasksAPIView.as_view()),
]
