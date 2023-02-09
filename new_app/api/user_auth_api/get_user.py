from rest_framework.response import Response
from new_app.serializers import UserSerializer
from django.forms.models import model_to_dict
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

# Get User API
class UserAPI(BaseUserAuthApi):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        print(self.request.user)
        response = baseHttpResponse()
        response.user = model_to_dict(self.request.user)
        return Response(response.dict())

    def get_object(self):
        print(self.request.user)
        return self.request.user