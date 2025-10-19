from django.urls import path
from .views import TextAnalysisTopicListView, AnalysisTextByTopicView, AnalysisTextDetailView

urlpatterns = [
    path('topics/', TextAnalysisTopicListView.as_view(), name='text-analysis-topic-list'),
    path('texts/', AnalysisTextByTopicView.as_view(), name='text-by-topic'),
    path('texts/<int:pk>/', AnalysisTextDetailView.as_view(), name='text-detail'),
]