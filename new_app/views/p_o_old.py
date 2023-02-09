import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

class PromptOptimizerView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
            res = {
                # "current_user": current_user_data,
                "input": prompt,
                "selected_model": "Privacy model 1",
                "selected_ai_model": "ChatGpt By Open AI",
                "output": prompt + ' final'
            }
            return JsonResponse({
                'err': 0,
                'errMessage': '',
                'results': res,
            }, safe=False)
        else:
            return JsonResponse({
                'err': 1,
                'errMessage': ' no user logged in',
            }, safe=False)