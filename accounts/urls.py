from django.urls import path
from accounts.views import (
    RegisterApiView,
    RegisterVerifyApiView,
    ResendVerifyCodeApiView,
    PasswordResetRequestApiView,
    PasswordResetApiView,
)

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('register/verify/', RegisterVerifyApiView.as_view()),
    path('register/resend-code/', ResendVerifyCodeApiView.as_view()),
    path('password/reset-request/', PasswordResetRequestApiView.as_view()),
    path('password/reset/', PasswordResetApiView.as_view()),
]