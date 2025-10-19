# fill_in_blank/models.py
from django.db import models
from django.conf import settings

class FillInBlankTopic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Fill-in-the-Blank Topic"
        verbose_name_plural = "Fill-in-the-Blank Topics"


class FillInBlankText(models.Model):
    topic = models.ForeignKey(FillInBlankTopic, on_delete=models.CASCADE, related_name='texts')
    title = models.CharField(max_length=255, blank=True, null=True)
    instruction_text = models.TextField(
        default="Read the text below and fill in the blanks with appropriate words."
    )
    text_content = models.TextField(help_text="Use '[[BLANK]]' for each blank.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or self.topic.name} ({self.topic.name})"


class BlankAnswer(models.Model):
    fill_in_blank_text = models.ForeignKey(FillInBlankText, on_delete=models.CASCADE, related_name='answers')
    blank_index = models.IntegerField(help_text="Position of the blank (0-indexed)")
    correct_answer = models.CharField(max_length=200)

    class Meta:
        unique_together = ('fill_in_blank_text', 'blank_index')

    def __str__(self):
        return f"Blank {self.blank_index}: {self.correct_answer}"

class FillInBlankResult(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fill_in_blank_results'
    )
    fill_in_blank_text = models.ForeignKey(
        FillInBlankText,
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField(help_text="Number of correct answers")
    total = models.PositiveIntegerField(help_text="Total number of blanks")
    percentage = models.FloatField(help_text="Score as percentage")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fill-in-the-Blank Result"
        verbose_name_plural = "Fill-in-the-Blank Results"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} - {self.fill_in_blank_text.title or self.fill_in_blank_text.id} ({self.score}/{self.total})"