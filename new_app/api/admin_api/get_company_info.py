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


class GetCompanyInfoApi(BaseAdminAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        response = baseHttpResponse()
        company_domain = request.data['domain']
        offset = request.data['offset']
        limit = request.data['limit']
        ip_address = self.get_client_ip(request=request)

        company = False
        try:
            company = Company.objects.get(domain=company_domain)
        except:
            pass
        if not company:
            response.err = 1
            response.errMessage = 'Unauthorized'
            return JsonResponse(response.dict(), safe=False)

        response.company_total_prompts = UserPrompt.objects.filter(user__company=company).count()
        response.company_total_privacy_model_prompts = UserPrivacyModelPrompt.objects.filter(company=company).count()

        response.company_total_users = User.objects.filter(company=company).count()
        start = offset * limit
        end = start + limit
        company_users = User.objects.filter(company=company)[start:end] \
            .values("id", "username", "email")
        response.company_users = list(company_users)
        # # https://riptutorial.com/django/example/30595/groub-by-----count-sum-django-orm-equivalent
        company_top_prompt_users = UserPrompt.objects.filter(user__company=company).values('user__id', 'user__email') \
            .annotate(count=Count('user__id'), sum=Sum('user__id')) \
            .order_by('-count')
        response.company_top_prompt_users = list(company_top_prompt_users)

        company_top_privacy_prompt_users = UserPrivacyModelPrompt.objects.filter(company=company).values('user__id', 'user__email') \
            .annotate(count=Count('user__id'), sum=Sum('user__id')) \
            .order_by('-count')
        response.company_top_privacy_prompt_users = list(company_top_privacy_prompt_users)

        return JsonResponse(response.dict(), safe=False)
