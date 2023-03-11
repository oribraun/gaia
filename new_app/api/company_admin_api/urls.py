from .get_users import GetUsersApi
from .get_user_info import GetUserInfoApi
from .get_user_prompts import GetCompanyUserPromptsApi
from .get_user_privacy_modelprompts import GetCompanyUserPrivacyModelPromptsApi
from django.urls import path, re_path, include

prefix = 'co'
urlpatterns = [
    path('get-users', GetUsersApi.as_view(), name=f'{prefix}-get-users'),
    path('get-user-info', GetUserInfoApi.as_view(), name=f'{prefix}-get-user-info'),
    path('get-user-prompts', GetCompanyUserPromptsApi.as_view(), name=f'{prefix}-get-user-prompts'),
    path('get-user-privacy-model-prompts', GetCompanyUserPrivacyModelPromptsApi.as_view(), name=f'{prefix}-get-user-privacy-model-prompts')
]