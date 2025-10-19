# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Import result models from all apps
from grammar_test.models import GrammarResult
from fill_in_blanks.models import FillInBlankResult
from match_synonyms.models import SynonymResult

# === Grammar Result Inline ===
class GrammarResultInline(admin.TabularInline):
    model = GrammarResult
    extra = 0
    readonly_fields = ('topic', 'score', 'total_questions', 'created_at')
    can_delete = False
    verbose_name = "Grammar Test Result"
    verbose_name_plural = "Grammar Test Results"
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return False

# === Fill-in-the-Blank Result Inline ===
class FillInBlankResultInline(admin.TabularInline):
    model = FillInBlankResult
    extra = 0
    readonly_fields = ('fill_in_blank_text', 'score', 'total', 'percentage', 'submitted_at')
    can_delete = False
    verbose_name = "Fill-in-the-Blank Result"
    verbose_name_plural = "Fill-in-the-Blank Results"
    ordering = ('-submitted_at',)

    def has_add_permission(self, request, obj=None):
        return False

# === Synonym Result Inline ===
class SynonymResultInline(admin.TabularInline):
    model = SynonymResult
    extra = 0
    readonly_fields = ('topic', 'score', 'total', 'percentage', 'submitted_at')
    can_delete = False
    verbose_name = "Synonym Match Result"
    verbose_name_plural = "Synonym Match Results"
    ordering = ('-submitted_at',)

    def has_add_permission(self, request, obj=None):
        return False

# === Custom User Admin ===
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Your existing fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Profile', {'fields': ('name', 'role', 'first_name', 'last_name')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'role', 'is_active', 'is_staff'),
        }),
    )

    list_display = ('username', 'name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'name')
    ordering = ('username',)

    # 👇 Add all result inlines here
    inlines = [
        GrammarResultInline,
        FillInBlankResultInline,
        SynonymResultInline,
    ]

# Unregister Group (as before)
from django.contrib.auth.models import Group
admin.site.unregister(Group)
admin.site.site_header = "Creative teacher Admin"
admin.site.site_title = "Creative teacher Admin Portal"
admin.site.index_title = "Welcome to Creative teacher Admin"