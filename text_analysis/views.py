# tex_analysis/views.py
from rest_framework import generics
from .models import TextAnalysisTopic, AnalysisText
from .serializers import TextAnalysisTopicSerializer, AnalysisTextSerializer


class TextAnalysisTopicListView(generics.ListAPIView):
    """
    API endpoint that returns a list of all text analysis topics.
    URL: GET /api/texts/topics/
    """
    queryset = TextAnalysisTopic.objects.all()
    serializer_class = TextAnalysisTopicSerializer
    # Authentication handled globally via JWT in settings.py


class AnalysisTextByTopicView(generics.ListAPIView):
    """
    API endpoint that returns all AnalysisText entries for a given topic.
    URL: GET /api/texts/texts/?topic_id=1
    """
    serializer_class = AnalysisTextSerializer

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        if topic_id and topic_id.isdigit():
            return AnalysisText.objects.filter(topic_id=topic_id)
        return AnalysisText.objects.none()


class AnalysisTextDetailView(generics.RetrieveAPIView):
    """
    API endpoint that returns a single AnalysisText by ID.
    URL: GET /api/texts/texts/<id>/
    """
    queryset = AnalysisText.objects.all()
    serializer_class = AnalysisTextSerializer
    lookup_field = 'pk'