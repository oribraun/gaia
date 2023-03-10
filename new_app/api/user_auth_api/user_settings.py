import random
from django.http import HttpResponse, JsonResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.user_setting import UserSetting


class UserSetSettingsApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        response = baseHttpResponse()
        key = request.data['key']
        data = request.data['data']
        ip_address = self.get_client_ip(request=request)
        user = request.user
        try:
            s = UserSetting.objects.get(user=user, key=key)
            s.data = data
            s.save()
        except:
            UserSetting.objects.create(user=request.user, key=key, data=data)

        return JsonResponse(response.dict(), safe=False)

class UserGetSettingsApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        response = baseHttpResponse()
        key = request.data['key']
        # ip_address = self.get_client_ip(request=request)
        user = request.user
        data = []
        try:
            data = UserSetting.objects.values_list('data', flat=True).get(user=user, key=key)
        except:
            pass
        response.data = data
        return JsonResponse(response.dict(), safe=False)