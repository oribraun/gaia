import random
from django.core import serializers
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from .base_api import BaseCompanyAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user import User
from new_app.app_models.company_admin import CompanyAdmin


class GetUsersApi(BaseCompanyAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        company_users_offset = 0
        company_users_limit = 10

        response = self.get_users(request, company_users_offset, company_users_limit)

        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        company_users_offset = request.data['company_users_offset']
        company_users_limit = request.data['company_users_limit']

        response = self.get_users(request, company_users_offset, company_users_limit)

        return JsonResponse(response.dict(), safe=False)

    def get_users(self, request, company_users_offset, company_users_limit):
        response = baseHttpResponse()
        user = request.user
        company = user.company

        ip_address = self.get_client_ip(request=request)
        start = company_users_offset * company_users_limit
        end = start + company_users_limit
        company_users = User.objects.filter(company=company)[start:end].values("id", "username", "email")
        response.company_users = list(company_users)
        return response
