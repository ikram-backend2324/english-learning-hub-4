# match_synonyms/models.py
from django.db import models
from django.conf import settings

class SynonymTopic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Synonym Topic"
        verbose_name_plural = "Synonym Topics"


class SynonymPair(models.Model):
    topic = models.ForeignKey(SynonymTopic, on_delete=models.CASCADE, related_name='pairs')
    word = models.CharField(max_length=100)
    synonym = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('topic', 'word')  # Prevent duplicate words in same topic

    def __str__(self):
        return f"{self.word} → {self.synonym}"

class SynonymResult(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='synonym_results'
    )
    topic = models.ForeignKey(
        SynonymTopic,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField(help_text="Number of correct matches")
    total = models.PositiveIntegerField(help_text="Total number of words in the topic")
    percentage = models.FloatField(help_text="Score as percentage")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Synonym Result"
        verbose_name_plural = "Synonym Results"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} - {self.topic.name} ({self.score}/{self.total})"
