from rest_framework import generics, permissions
from new_app.api.base_api import BaseApi
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company_admin import CompanyAdmin
from django.http import HttpResponse, JsonResponse

class BaseUserAuthApi(BaseApi):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [permissions.IsAuthenticated,]

    def dispatch(self, request, *args, **kwargs):
        response = baseHttpResponse()
        user = request.user
        company = user.company
        is_admin = user.is_superuser
        company_admin = False
        try:
            company_admin = CompanyAdmin.objects.get(user=user).__dict__
        except:
            pass
        if not company_admin:
            response.err = 1
            response.errMessage = 'Unauthorized'
            return JsonResponse(response.dict(), safe=False)

        return super().dispatch(request, *args, **kwargs)