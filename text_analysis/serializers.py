from rest_framework import serializers
from .models import TextAnalysisTopic, AnalysisText, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'created_at']

class AnalysisTextSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = AnalysisText
        fields = [
            'id',
            'title',
            'topic',          # ID of TextAnalysisTopic
            'topic_name',     # Human-readable name
            'instruction_text',
            'text_content',
            'created_at',
            'questions'
        ]

class TextAnalysisTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnalysisTopic
        fields = ['id', 'name', 'created_at']