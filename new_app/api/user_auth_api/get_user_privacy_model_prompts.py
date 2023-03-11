import random
from django.core import serializers
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from new_app.api.user_auth_api.base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt
from new_app.app_models.user import User
from new_app.app_models.company_admin import CompanyAdmin


class GetUserPrivacyModelPromptsApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        response = baseHttpResponse()
        user_prompts_offset = request.data['offset']
        user_prompts_limit = request.data['limit']
        user = request.user
        company = user.company
        ip_address = self.get_client_ip(request=request)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        start = user_prompts_offset * user_prompts_limit
        end = start + user_prompts_limit
        user_prompts = UserPrivacyModelPrompt.objects.filter(user=user)[start:end] \
            .values("prompt")
        response.user_prompts = list(user_prompts)
        return JsonResponse(response.dict(), safe=False)
