from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class GrammarTopic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 👈 Add this

    def __str__(self):
        return self.name


class GrammarQuestion(models.Model):
    topic = models.ForeignKey(GrammarTopic, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    created_at = models.DateTimeField(auto_now_add=True)  # 👈 Add this

    def __str__(self):
        return self.question_text
    @property
    def correct_answer(self):
        mapping = {
            'A': self.option_a,
            'B': self.option_b,
            'C': self.option_c,
            'D': self.option_d,
        }
        return mapping.get(self.correct_option, "")

class GrammarResult(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grammar_results'
    )
    topic = models.ForeignKey(
        'GrammarTopic',  # or your actual topic model name
        on_delete=models.CASCADE,
        related_name='results'
    )
    score = models.PositiveIntegerField(help_text="Number of correct answers")
    total_questions = models.PositiveIntegerField(help_text="Total number of questions")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Grammar Result"
        verbose_name_plural = "Grammar Results"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} - {self.topic.name}: {self.score}/{self.total_questions}"
