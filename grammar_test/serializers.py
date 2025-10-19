from rest_framework import serializers
from .models import GrammarTopic, GrammarQuestion, GrammarResult

class GrammarQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarQuestion
        fields = '__all__'


class GrammarTopicSerializer(serializers.ModelSerializer):
    questions = GrammarQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = GrammarTopic
        fields = ['id', 'name', 'questions']


class GrammarResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarResult
        fields = '__all__'
        read_only_fields = ['student']

