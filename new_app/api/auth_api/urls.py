from django.urls import path, re_path, include
from .auth import *
from new_app.views.password_reset_confirm import PasswordResetConfirmView, VerifyEmailView
from new_app.api.user_auth_api.get_user import UserAPI
from new_app.api.user_auth_api.change_password import ChangePasswordApi

prefix = 'auth'
API_AUTH_BASE = ''
urlpatterns = [
    path('register', RegisterAPI.as_view(), name=f'{prefix}-register'),
    path('login', LoginAPI.as_view(), name=f'{prefix}-login'),
    path('logout', LogoutAPI.as_view(), name=f'{prefix}-logout'),
    # path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('forgot-pass', ForgotPasswordAPI.as_view(), name=f'{prefix}-forgot-pass'),
    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name=f'password_reset_confirm'),
    path('verify-email/<uidb64>/<token>', VerifyEmailView.as_view(), name=f'{prefix}-verify_email'),
    path('resend_verify_email', ResendVerifyEmailApi.as_view(), name=f'{prefix}-resend_verify_email'),
    path('user', UserAPI.as_view(), name=f'{prefix}-user'),
    path('change-password', ChangePasswordApi.as_view(), name=f'{prefix}-change-password'),
]