from rest_framework import generics, permissions
from new_app.api.base_api import BaseApi
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication

class BaseUserAuthApi(BaseApi):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [permissions.IsAuthenticated,]