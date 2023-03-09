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
            company_admin = CompanyAdmin.objects.get(user=user).__dict__
        except:
            pass

        get_only_gaia_admin_data = False
        all = self.getAll(
            request= request,
            type='user_prompts',
            offset=0,
            limit=10,
            is_company_admin=(True if company_admin else False),
            is_gaia_admin=is_admin,
            admin_only=get_only_gaia_admin_data
        )
        if all:
            response.data = list(all.values())
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        response = baseHttpResponse()
        user = request.user
        company = user.company
        is_gaia_admin = user.is_superuser
        company_admin = False
        try:
            CompanyAdmin.objects.get(user=user)
            company_admin = True
        except:
            pass

        ip_address = self.get_client_ip(request=request)

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrompt.objects.all()
        # user_prompt = UserPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        user_prompts_offset = 0
        user_prompts_limit = 10
        company_users_offset = 0
        company_users_limit = 10
        admin_company_offset = 0
        admin_company_limit = 10
        response.total_user_prompts = UserPrompt.objects.filter(user=user).count()
        user_prompts = UserPrompt.objects.filter(user=user)[user_prompts_offset:user_prompts_offset + user_prompts_limit]\
                .values("prompt")
        response.user_prompts = list(user_prompts)
        response.results_type = 'user'
        response.company_admin = company_admin
        if company:
            response.results_type = 'company_user'
            response.company_total_prompts = UserPrompt.objects.filter(user__company=company).count()
            response.company_total_privacy_model_prompts = UserPrivacyModelPrompt.objects.filter(company=company).count()
        print('company_admin', company_admin)
        if company_admin:
            response.results_type = 'company_admin'
            response.company_total_users = User.objects.filter(company=company).count()
            company_users = User.objects.filter(company=company)[company_users_offset:company_users_offset + company_users_limit]\
                .values("id", "username", "email")
            response.company_users = list(company_users)
            # https://riptutorial.com/django/example/30595/groub-by-----count-sum-django-orm-equivalent
            company_top_prompt_users = UserPrompt.objects.values('user__id', 'user__email')\
                .annotate(count=Count('user__id'), sum=Sum('user__id'))\
                .order_by('-count')
            response.company_top_prompt_users = list(company_top_prompt_users)

            company_top_privacy_prompt_users = UserPrivacyModelPrompt.objects.values('user__id', 'user__email')\
                .annotate(count=Count('user__id'), sum=Sum('user__id'))\
                .order_by('-count')
            response.company_top_privacy_prompt_users = list(company_top_privacy_prompt_users)
        if is_gaia_admin:
            companies = Company.objects.all()[admin_company_offset:admin_company_offset + admin_company_limit]\
                .values("id", "name", "domain")
            response.companies = list(companies)
            response.total_companies = Company.objects.all().count()
            response.results_type = 'gaia_admin'

        # user_prompts = self.getAll(
        #     request=request,
        #     type='user_prompts',
        #     offset=0,
        #     limit=10,
        #     is_company_admin=(True if company_admin else False),
        #     is_gaia_admin=is_gaia_admin,
        #     admin_only=True
        # )
        # if user_prompts:
        #     response.results_type = results_type
        #     response.data = list(user_prompts.values())
        #     response.user = serializers.serialize('json', [user])
        return JsonResponse(response.dict(), safe=False)

    def getAll(self, request, type, offset, limit, is_company_admin, is_gaia_admin, admin_only=False):
        results = []
        user = request.user
        print('user', user)
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
