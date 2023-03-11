import random
from django.core import serializers
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from .base_api import BaseAdminAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user import User
from new_app.app_models.company_admin import CompanyAdmin


class GetCompaniesApi(BaseAdminAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        company_users_offset = 0
        company_users_limit = 10

        response = self.get_companies(request, company_users_offset, company_users_limit)

        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        company_offset = request.data['offset']
        company_limit = request.data['limit']

        response = self.get_companies(request, company_offset, company_limit)

        return JsonResponse(response.dict(), safe=False)

    def get_companies(self, request, company_offset, company_limit):
        response = baseHttpResponse()
        user = request.user
        company = user.company

        ip_address = self.get_client_ip(request=request)
        start = company_offset * company_limit
        end = start + company_limit
        companies = Company.objects.filter()[start:end].values("id", "name", "domain")
        response.companies = list(companies)
        return response
