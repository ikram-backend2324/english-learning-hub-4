from django.contrib import admin
from .models import FillInBlankTopic, FillInBlankText, BlankAnswer, FillInBlankResult

class FillInBlankResultInline(admin.TabularInline):
    model = FillInBlankResult
    extra = 0
    readonly_fields = ('fill_in_blank_text', 'score', 'total', 'percentage', 'submitted_at')
    can_delete = False

@admin.register(FillInBlankTopic)
class FillInBlankTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(FillInBlankText)
class FillInBlankTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'created_at')
    list_filter = ('topic',)
    search_fields = ('title', 'text_content')
    fields = ('topic', 'title', 'instruction_text', 'text_content')

@admin.register(BlankAnswer)
class BlankAnswerAdmin(admin.ModelAdmin):
    list_display = ('fill_in_blank_text', 'blank_index', 'correct_answer')
    list_filter = ('fill_in_blank_text__topic',)
    search_fields = ('correct_answer', 'fill_in_blank_text__title')

@admin.register(FillInBlankResult)
class FillInBlankResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'text_title', 'score', 'total', 'percentage', 'submitted_at')
    list_filter = ('student', 'fill_in_blank_text__topic', 'submitted_at')
    readonly_fields = ('student', 'fill_in_blank_text', 'score', 'total', 'percentage', 'submitted_at')

    def text_title(self, obj):
        return obj.fill_in_blank_text.title or str(obj.fill_in_blank_text.id)
    text_title.short_description = "Text"

