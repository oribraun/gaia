import random
from django.http import HttpResponse, JsonResponse
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

from privacy_classifier.pipeline.pipeline import PrivacyClassifierPipeline
pipeline = PrivacyClassifierPipeline()

class PrivacyModelApi(BaseUserAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = baseHttpResponse()
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        boolean = random.choice([True, False])
        prompt = request.data['prompt']
        res = pipeline(text=prompt)
        return JsonResponse({
            'err': 0,
            'errMessage': '',
            'model_res': res,
            'suggested_prompt': prompt + ' suggested',
            'suggested_model': ' Privacy model V1',
            'pass_privacy': False,
        }, safe=False)