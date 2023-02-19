import random
from django.http import HttpResponse, JsonResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user_prompt import UserPrompt
from new_app.app_models.user import User
from new_app.app_models.company_admin import CompanyAdmin


class GetDashboardApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = baseHttpResponse()
        user = request.user
        company = user.company
        is_admin = user.is_superuser
        company_admin = False
        try:
            company_admin = CompanyAdmin.objects.get(company=company)
        except:
            pass

        all = self.getAll(
            request= request,
            type='user_prompts',
            offset=0,
            limit=10,
            is_company_admin=(True if company_admin else False),
            is_gaia_admin=is_admin,
            admin_only=True
        )
        if all:
            response.data = list(all.values())
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        prompt = request.data['prompt']
        ip_address = self.get_client_ip(request=request)
        user = request.user
        company = user.company
        if not company:
            UserPrompt.objects.create(user=request.user, prompt=prompt, ip_address=ip_address)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        return JsonResponse({
            'err': 0,
            'errMessage': ''
        }, safe=False)

    def getAll(self, request, type, offset, limit, is_company_admin, is_gaia_admin, admin_only=False):
        results = None
        user = request.user
        company = user.company
        if is_gaia_admin and not admin_only:
            user = None
        if not company or is_gaia_admin:
            if type == 'user_prompts':
                if user:
                    results = UserPrompt.objects.filter(user=user)[offset:offset+limit]
                else:
                    results = UserPrompt.objects.filter()[offset:offset + limit]
        if is_company_admin:
            user = None
        if company and not len(results):
            if type == 'privacy_model_prompt':
                results = UserPrompt.objects.filter(user=user, company=company)[offset:offset+limit]
            if type == 'users' and is_company_admin:
                results = User.objects.filter(company=company)[offset:offset+limit]

        return results
