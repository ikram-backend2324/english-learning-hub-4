from django.contrib import admin
from .models import SynonymTopic, SynonymPair, SynonymResult

@admin.register(SynonymTopic)
class SynonymTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(SynonymPair)
class SynonymPairAdmin(admin.ModelAdmin):
    list_display = ('word', 'synonym', 'topic')
    list_filter = ('topic',)
    search_fields = ('word', 'synonym')

@admin.register(SynonymResult)
class SynonymResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'score', 'total', 'percentage', 'submitted_at')
    list_filter = ('student', 'topic', 'submitted_at')
    readonly_fields = ('student', 'topic', 'score', 'total', 'percentage', 'submitted_at')
    search_fields = ('student__username', 'topic__name')