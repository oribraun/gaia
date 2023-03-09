from .get_users import GetUsersApi
from .get_user_info import GetUserInfoApi
from django.urls import path, re_path, include

urlpatterns = [
    path('get-users', GetUsersApi.as_view(), name='ca-get-users'),
    path('get-user-info', GetUserInfoApi.as_view(), name='ca-get-user-info')
]