# accounts/urls.py
from django.urls import path
from .views import LoginView, ProtectedView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),  # ❌ COMMENT OUT
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]
