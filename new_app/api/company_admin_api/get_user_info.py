import random
from django.core import serializers
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user import User
from new_app.app_models.company_admin import CompanyAdmin


class GetUserInfoApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_email = 'ori@gaialabs.ai'
        user_prompts_offset = 0
        user_prompts_limit = 10
        user = request.user
        company = user.company

        ip_address = self.get_client_ip(request=request)

        response = self.get_user_info(request, user_email, user_prompts_offset, user_prompts_limit)
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        user_email = request.data['user_email']
        user_prompts_offset = request.data['user_prompts_offset']
        user_prompts_limit = request.data['user_prompts_limit']
        user = request.user
        company = user.company

        ip_address = self.get_client_ip(request=request)

        response = self.get_user_info(request, user_email, user_prompts_offset, user_prompts_limit)
        return JsonResponse(response.dict(), safe=False)

    def get_user_info(self, request, user_email, user_prompts_offset, user_prompts_limit):
        response = baseHttpResponse()
        user = request.user
        company = user.company

        ip_address = self.get_client_ip(request=request)

        response.total_user_prompts = UserPrompt.objects.filter(user=user).count()
        user_prompts = UserPrompt.objects.filter(user=user)[
                       user_prompts_offset:user_prompts_offset + user_prompts_limit] \
            .values("prompt")
        response.user_prompts = list(user_prompts)
        return response
