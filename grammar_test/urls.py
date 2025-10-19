from django.urls import path
from .views import GrammarTopicListView, GrammarQuestionByTopicView, GrammarSubmitView, GrammarQuestionListView

urlpatterns = [
    path('topics/', GrammarTopicListView.as_view(), name='grammar-topics'),
    path('topics/<int:pk>/questions/', GrammarQuestionByTopicView.as_view(), name='grammar-topic-questions'),
    path('submit/', GrammarSubmitView.as_view(), name='grammar-submit'),
    path("questions/", GrammarQuestionListView.as_view(), name="questions"),

]
