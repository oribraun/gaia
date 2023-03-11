from django.contrib.auth.decorators import login_required
from knox import views as knox_views
from new_app.api.user_auth_api.change_password import ChangePasswordApi
# from new_app.views.get_data import get_data
from new_app.views.password_reset_confirm import PasswordResetConfirmView, VerifyEmailView
from new_app.api.public_api.public import PublicApi
from new_app.api.user_auth_api.privacy_model import PrivacyModelApi
from new_app.api.user_auth_api.collect_user_prompt import CollectUserPromptApi
from new_app.api.external_auth_api.prompt_optimizer import PromptOptimizerApi
from new_app.api.user_auth_api.get_user import UserAPI
from new_app.api.user_auth_api.upload_file import UploadFileApi
from new_app.api.user_auth_api.analyze import AnalyzeApi
from new_app.api.user_auth_api.get_dashboard import GetDashboardApi
from new_app.api.user_auth_api.chat_gpt_api import ChatGptApi
from new_app.api.user_auth_api.user_settings import UserGetSettingsApi, UserSetSettingsApi
from new_app.api.user_auth_api.get_user_prompts import GetUserPromptsApi
from new_app.api.auth import LoginAPI, RegisterAPI, LogoutAPI, ForgotPasswordAPI, ResendVerifyEmailApi
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt

API_BASE = 'api/'
API_AUTH_BASE = API_BASE + 'auth/'
urlpatterns = [
    # path('api/auth/', include('knox.urls')),
    # path(API_AUTH_BASE + 'register', RegisterAPI.as_view(), name='register'),
    # path(API_AUTH_BASE + 'login', LoginAPI.as_view(), name='login'),
    # path(API_AUTH_BASE + 'logout', LogoutAPI.as_view(), name='logout'),
    # path(API_AUTH_BASE + 'forgot-pass', ForgotPasswordAPI.as_view(), name='forgot-pass'),
    # path(API_AUTH_BASE + 'password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path(API_AUTH_BASE + 'verify-email/<uidb64>/<token>', VerifyEmailView.as_view(), name='verify_email'),
    # path(API_AUTH_BASE + 'resend_verify_email', ResendVerifyEmailApi.as_view(), name='resend_verify_email'),
    # path(API_AUTH_BASE + 'user', UserAPI.as_view(), name='user'),
    # path(API_AUTH_BASE + 'change-password', ChangePasswordApi.as_view(), name='change-password'),

    # path(API_AUTH_BASE + 'logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),

    # re_path(r'^getData/(\d+)$', get_data),
    # re_path(r'^getData', login_required(get_data)),

    re_path(rf'^{API_BASE}prompt_optimizer$', PromptOptimizerApi.as_view()),
    # re_path(rf'^{API_BASE}upload$', UploadFileApi.as_view()),
    # re_path(rf'^{API_BASE}analyze$', AnalyzeApi.as_view()),
    # re_path(rf'^{API_BASE}privacy-model$', PrivacyModelApi.as_view()),
    # re_path(rf'^{API_BASE}collect-user-prompt$', CollectUserPromptApi.as_view()),
    # re_path(rf'^{API_BASE}get-dashboard$', GetDashboardApi.as_view()),
    # re_path(rf'^{API_BASE}get-answer$', ChatGptApi.as_view()),
    # re_path(rf'^{API_BASE}set-settings$', UserSetSettingsApi.as_view()),
    # re_path(rf'^{API_BASE}get-settings$', UserGetSettingsApi.as_view()),
    # re_path(rf'^{API_BASE}get-user-prompts$', GetUserPromptsApi.as_view()),
    re_path(rf'^{API_BASE}public$', PublicApi.as_view()),

    path(API_BASE + 'auth/', include('new_app.api.auth_api.urls'), name='auth'),

    path(API_BASE + 'co/', include('new_app.api.company_admin_api.urls'), name='company'),

    path(API_BASE + 'us/', include('new_app.api.user_auth_api.urls'), name='user'),

    path(API_BASE + 'adm/', include('new_app.api.admin_api.urls'), name='admin'),
]