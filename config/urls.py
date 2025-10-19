from django.contrib import admin
from django.urls import path, include
from accounts.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    # ✅ Mount apps correctly
    path('api/accounts/', include('accounts.urls')),
    path('api/grammar_test/', include('grammar_test.urls')),
    path('api/texts/', include('text_analysis.urls')),
    path('api/synonyms/', include('match_synonyms.urls')),
    path('api/fill_in_blanks/', include('fill_in_blanks.urls')),
    path('api/essays/', include('essay_writing.urls')),
]