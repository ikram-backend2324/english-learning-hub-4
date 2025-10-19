from rest_framework import serializers
from .models import EssayTopic, EssaySubmission

class EssayTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayTopic
        fields = ['id', 'name', 'instruction_text', 'word_count_min', 'word_count_max']

class EssaySubmissionSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = EssaySubmission
        fields = ['id', 'topic', 'topic_name', 'student_name', 'essay_text', 'submitted_at']