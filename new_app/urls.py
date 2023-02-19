from django.contrib.auth.decorators import login_required
from knox import views as knox_views
from new_app.api.user_auth_api.change_password import ChangePasswordApi
# from new_app.views.get_data import get_data
from new_app.views.password_reset_confirm import PasswordResetConfirmView
from new_app.api.public_api.public import PublicApi
from new_app.api.user_auth_api.privacy_model import PrivacyModelApi
from new_app.api.user_auth_api.collect_user_prompt import CollectUserPromptApi
from new_app.api.external_auth_api.prompt_optimizer import PromptOptimizerApi
from new_app.api.user_auth_api.get_user import UserAPI
from new_app.api.user_auth_api.upload_file import UploadFileApi
from new_app.api.user_auth_api.analyze import AnalyzeApi
from new_app.api.user_auth_api.get_dashboard import GetDashboardApi
from new_app.api.auth import LoginAPI, RegisterAPI, LogoutAPI, ForgotPasswordAPI
from django.urls import path, re_path, include

API_BASE = 'api/'
API_AUTH_BASE = API_BASE + 'auth/'
urlpatterns = [
    # path('api/auth/', include('knox.urls')),
    path(API_AUTH_BASE + 'register', RegisterAPI.as_view(), name='register'),
    path(API_AUTH_BASE + 'login', LoginAPI.as_view(), name='login'),
    path(API_AUTH_BASE + 'logout', LogoutAPI.as_view(), name='logout'),
    # path(API_AUTH_BASE + 'logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path(API_AUTH_BASE + 'forgot-pass', ForgotPasswordAPI.as_view(), name='forgot-pass'),
    path(API_AUTH_BASE + 'password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(API_AUTH_BASE + 'user', UserAPI.as_view(), name='user'),
    path(API_AUTH_BASE + 'change-password', ChangePasswordApi.as_view(), name='change-password'),
    # re_path(r'^getData/(\d+)$', get_data),
    # re_path(r'^getData', login_required(get_data)),
    re_path(rf'^{API_BASE}prompt_optimizer$', PromptOptimizerApi.as_view()),
    re_path(rf'^{API_BASE}upload$', UploadFileApi.as_view()),
    re_path(rf'^{API_BASE}analyze$', AnalyzeApi.as_view()),
    re_path(rf'^{API_BASE}privacy-model$', PrivacyModelApi.as_view()),
    re_path(rf'^{API_BASE}collect-user-prompt$', CollectUserPromptApi.as_view()),
    re_path(rf'^{API_BASE}get-dashboard$', GetDashboardApi.as_view()),
    re_path(rf'^{API_BASE}public$', PublicApi.as_view()),
]