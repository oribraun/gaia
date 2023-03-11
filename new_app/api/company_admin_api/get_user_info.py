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


class GetUserInfoApi(BaseCompanyAuthApi):
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
        selected_item = request.data['selectedItem']
        user_email = selected_item['email']
        user_prompts_offset = request.data['offset']
        user_prompts_limit = request.data['limit']

        ip_address = self.get_client_ip(request=request)

        response = self.get_user_info(request, user_email, user_prompts_offset, user_prompts_limit)
        return JsonResponse(response.dict(), safe=False)

    def get_user_info(self, request, user_email, user_prompts_offset, user_prompts_limit):
        response = baseHttpResponse()

        ip_address = self.get_client_ip(request=request)

        response.total_user_prompts = UserPrompt.objects.filter(user__email=user_email).count()
        start = user_prompts_offset * user_prompts_limit
        end = start + user_prompts_limit
        user_prompts = UserPrompt.objects.filter(user__email=user_email)[start:end].values("prompt")
        response.user_prompts = list(user_prompts)

        response.total_user_privacy_model_prompts = UserPrivacyModelPrompt.objects.filter(
            user__email=user_email).count()
        start = user_prompts_offset * user_prompts_limit
        end = start + user_prompts_limit
        user_privacy_model_prompts = UserPrivacyModelPrompt.objects.filter(user__email=user_email)[start:end] \
            .values("prompt")
        response.user_privacy_model_prompts = list(user_privacy_model_prompts)

        return response
