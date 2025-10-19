# essay_writing/models.py
from django.db import models

class EssayTopic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    instruction_text = models.TextField(
        help_text="Instructions for the essay (e.g., word count, structure)"
    )
    word_count_min = models.IntegerField(default=300)
    word_count_max = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Essay Topic"
        verbose_name_plural = "Essay Topics"


class EssaySubmission(models.Model):
    topic = models.ForeignKey(EssayTopic, on_delete=models.CASCADE, related_name='submissions')
    student_name = models.CharField(max_length=255)
    essay_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.topic.name}"

    class Meta:
        ordering = ['-submitted_at']