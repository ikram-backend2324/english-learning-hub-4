from django.urls import path
from .views import (
    SynonymTopicListView,
    SynonymPairByTopicView,
    SynonymSubmitView
)

urlpatterns = [
    path('topics/', SynonymTopicListView.as_view(), name='synonym-topic-list'),
    path('pairs/', SynonymPairByTopicView.as_view(), name='synonym-pairs-by-topic'),
    path('submit/', SynonymSubmitView.as_view(), name='synonym-submit'),
]