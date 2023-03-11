from django.urls import path, re_path, include

from .user_settings import UserSetSettingsApi, UserGetSettingsApi
from .get_user_prompts import GetUserPromptsApi
from .get_dashboard import GetDashboardApi
from .analyze import AnalyzeApi
from .change_password import ChangePasswordApi
from .chat_gpt_api import ChatGptApi
from .collect_user_prompt import CollectUserPromptApi
from .get_user import UserAPI
from .privacy_model import PrivacyModelApi
from .upload_file import UploadFileApi

prefix = 'us'
urlpatterns = [
    path('get-dashboard', GetDashboardApi.as_view(), name=f'{prefix}-get-dashboard'),
    path('analyze', AnalyzeApi.as_view(), name=f'{prefix}-analyze'),
    # path('change-password', ChangePasswordApi.as_view(), name=f'{prefix}-change-password'),
    path('get-answer', ChatGptApi.as_view(), name=f'{prefix}-get-answer'),
    path('collect-user-prompt', CollectUserPromptApi.as_view(), name=f'{prefix}-collect-user-prompt'),
    path('privacy-model', PrivacyModelApi.as_view(), name=f'{prefix}-privacy-model'),
    path('upload$', UploadFileApi.as_view(), name=f'{prefix}-upload$'),
    path('set-settings', UserSetSettingsApi.as_view(), name=f'{prefix}-set-settings'),
    path('get-settings', UserGetSettingsApi.as_view(), name=f'{prefix}-get-settings'),
    path('get-user-prompts', GetUserPromptsApi.as_view(), name=f'{prefix}-get-user-prompts'),
    path('get-user-privacy-model-prompts', GetUserPromptsApi.as_view(), name=f'{prefix}-get-user-privacy-model-prompts'),
]