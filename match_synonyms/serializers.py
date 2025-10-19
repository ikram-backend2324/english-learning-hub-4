from rest_framework import serializers
from .models import SynonymTopic, SynonymPair

class SynonymTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynonymTopic
        fields = ['id', 'name']

class SynonymPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynonymPair
        fields = ['id', 'word', 'synonym']