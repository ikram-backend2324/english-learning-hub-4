from rest_framework import serializers
from .models import FillInBlankTopic, FillInBlankText, BlankAnswer

class FillInBlankTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillInBlankTopic
        fields = ['id', 'name']

class BlankAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankAnswer
        fields = ['blank_index', 'correct_answer']

class FillInBlankTextSerializer(serializers.ModelSerializer):
    answers = BlankAnswerSerializer(many=True, read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = FillInBlankText
        fields = [
            'id',
            'title',
            'topic',
            'topic_name',
            'instruction_text',
            'text_content',
            'created_at',
            'answers'
        ]