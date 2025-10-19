from django.contrib import admin
from .models import TextAnalysisTopic, AnalysisText, Question

@admin.register(TextAnalysisTopic)
class TextAnalysisTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(AnalysisText)
class AnalysisTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    list_filter = ('topic',)
    search_fields = ('title', 'text_content')
    fields = ('topic', 'title', 'instruction_text', 'text_content')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'analysis_text', 'created_at')
    list_filter = ('analysis_text__topic',)
    search_fields = ('question_text', 'analysis_text__title')