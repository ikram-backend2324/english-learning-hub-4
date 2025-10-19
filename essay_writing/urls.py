from django.urls import path
from .views import EssayTopicListView, EssaySubmitView, EssayTopicDetailView

urlpatterns = [
    path('topics/', EssayTopicListView.as_view(), name='essay-topic-list'),
    path('submit/', EssaySubmitView.as_view(), name='essay-submit'),
    path('topics/<int:pk>/', EssayTopicDetailView.as_view(), name='essay-topic-detail'),
]