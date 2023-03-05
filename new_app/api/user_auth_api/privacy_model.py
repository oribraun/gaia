import random
from django.http import HttpResponse, JsonResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse
from new_app.app_models.company import Company
from new_app.app_models.user import User
from new_app.app_models.user_privacy_model_prompt import UserPrivacyModelPrompt

# from privacy_classifier.pipeline.pipeline import PrivacyClassifierPipeline
# pipeline = PrivacyClassifierPipeline()

class PrivacyModelApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = baseHttpResponse()
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        boolean = random.choice([True, False])
        prompt = request.data['prompt']
        ip = self.get_client_ip(request=request)
        gaia_ai_token = ''
        user = request.user
        company = user.company
        # print('company', company)
        # company_id = ''
        # company = ''
        # return HttpResponse('Forbidden', status=403)
        # if 'GAIA-AI-TOKEN' in request.headers:
        #     gaia_ai_token = request.headers['GAIA-AI-TOKEN']
        #     try:
        #         company = Company.objects.get(key=gaia_ai_token)
        #     except:
        #         return HttpResponse('Forbidden', status=403)
        # else:
        #     return HttpResponse('Forbidden', status=403)
        # print('gaia_ai_token', gaia_ai_token)
        # print('company', company)
        # print('request_user', request.user)
        # print('prompt', prompt)

        # res = pipeline(text=prompt)
        return_obj = {
            'err': 0,
            'errMessage': '',
            'model_res': {},
            'suggested_prompt': prompt + ' suggested',
            'suggested_model': ' Privacy model V1',
            'pass_privacy': False,
        }
        # if not return_obj["pass_privacy"]:
        #     prompt = 'removed'
        UserPrivacyModelPrompt.objects.create(
            user=request.user,
            prompt=prompt,
            company=company,
            pass_privacy=return_obj["pass_privacy"]
        )

        # user_prompt.save()
        # print('user_prompt', user_prompt.user)
        # all_users_prompt = UserPrivacyModelPrompt.objects.all()
        # user_prompt = UserPrivacyModelPrompt.objects.filter(user=request.user)
        # print('all_users_prompt', all_users_prompt.values())
        # print('user_prompt', user_prompt.values())
        return JsonResponse(return_obj, safe=False)