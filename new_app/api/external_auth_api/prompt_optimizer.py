import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .base_api import BaseExternalAuthApi
from new_app.api.jsonResponse import baseHttpResponse

class PromptOptimizerApi(BaseExternalAuthApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            response = baseHttpResponse()
            return JsonResponse(response.dict(), safe=False)
        else:
            response = baseHttpResponse()
            response.errMessage = 'no user logged in'
            return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        tembel_ai_token = ''
        if 'TEMBEL-AI-TOKEN' in request.headers:
            tembel_ai_token = request.headers['TEMBEL-AI-TOKEN']
        print('request.user', request.user)
        print('tembel_ai_token', tembel_ai_token)
        if request.user.is_authenticated:
            current_user = request.user
            current_user.api_total_requests += 1
            current_user.save()
            # current_user_data = model_to_dict(current_user)
            prompt = request.data['prompt']
            response = baseHttpResponse()
            response.results = {
                'input': prompt,
                'selected_model': "Privacy model 1",
                'selected_ai_model':  "ChatGpt By Open AI",
                'output': prompt + ' final'
            }

            return JsonResponse(response.dict(), safe=False)
        else:
            return JsonResponse({
                'err': 1,
                'errMessage': ' no user logged in',
            }, safe=False)