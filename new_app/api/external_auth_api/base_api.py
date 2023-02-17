from rest_framework import generics, permissions
from new_app.api.base_api import BaseApi
class BaseExternalAuthApi(BaseApi):
    pass
    # permission_classes = [permissions.IsAuthenticated,]