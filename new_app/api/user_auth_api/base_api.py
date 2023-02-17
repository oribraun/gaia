from rest_framework import generics, permissions
from new_app.api.base_api import BaseApi

class BaseUserAuthApi(BaseApi):
    permission_classes = [permissions.IsAuthenticated,]