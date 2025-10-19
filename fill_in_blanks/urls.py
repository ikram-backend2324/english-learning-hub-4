from django.urls import path
from .views import (
    FillInBlankTopicListView,
    FillInBlankTextView,
    FillInBlankSubmitView,
    FillInBlankTextByTopicView
)

urlpatterns = [
    path('topics/', FillInBlankTopicListView.as_view(), name='fill-in-blank-topic-list'),
    path('texts/<int:pk>/', FillInBlankTextView.as_view(), name='fill-in-blank-text-detail'),
    path('submit/', FillInBlankSubmitView.as_view(), name='fill-in-blank-submit'),
    path('texts/', FillInBlankTextByTopicView.as_view(), name='fill-in-blank-texts-by-topic'),
]