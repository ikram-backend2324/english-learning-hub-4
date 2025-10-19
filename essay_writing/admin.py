from django.contrib import admin
from .models import EssayTopic, EssaySubmission

@admin.register(EssayTopic)
class EssayTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'word_count_min', 'word_count_max', 'created_at')
    search_fields = ('name',)
    fields = ('name', 'instruction_text', 'word_count_min', 'word_count_max')


@admin.register(EssaySubmission)
class EssaySubmissionAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'topic', 'submitted_at')
    list_filter = ('topic', 'submitted_at')
    search_fields = ('student_name', 'essay_text')
    readonly_fields = ('submitted_at',)

    # Custom display for essay text in admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['essay_text'].widget.attrs['rows'] = 20
        form.base_fields['essay_text'].widget.attrs['style'] = 'width: 100%;'
        return form