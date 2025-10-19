# grammar_test/admin.py
from django.contrib import admin
from .models import GrammarTopic, GrammarQuestion, GrammarResult

@admin.register(GrammarTopic)
class GrammarTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  # ✅ now exists

@admin.register(GrammarQuestion)
class GrammarQuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question_text', 'correct_answer', 'created_at')  # ✅ all exist
    list_filter = ('topic',)

@admin.register(GrammarResult)
class GrammarResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'score', 'total_questions', 'created_at')
    list_filter = ('student', 'topic', 'created_at')
    readonly_fields = ('student', 'topic', 'score', 'total_questions', 'created_at')