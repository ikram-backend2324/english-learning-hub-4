from django.db import models

class TextAnalysisTopic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Text Analysis Topic"
        verbose_name_plural = "Text Analysis Topics"


class AnalysisText(models.Model):
    topic = models.ForeignKey(
        TextAnalysisTopic,  # ← Now linked to namespaced model
        on_delete=models.CASCADE,
        related_name='texts'
    )

    title = models.CharField(max_length=255, blank=True)
    instruction_text = models.TextField(
        default="Read the following text carefully and analyze it on paper. Consider the themes, literary devices, character development, and writing style:"
    )
    text_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.topic.name})"

    def save(self, *args, **kwargs):
        if not self.title and self.topic:
            self.title = str(self.topic)  # or self.topic.name if it has a name field
        super().save(*args, **kwargs)


class Question(models.Model):
    analysis_text = models.ForeignKey(AnalysisText, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_text[:50]}... ({self.analysis_text.title})"