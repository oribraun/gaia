from django.http import HttpResponse, JsonResponse

import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_protect
def prompt_optimizer(request):
    if request.method == 'POST':
        print('request', request.user)
        if request.user.is_authenticated:
            current_user = request.user
            current_user.api_total_requests += 1
            current_user.save()
            # current_user_data = model_to_dict(current_user)
            body = json.loads(request.body)
            prompt = body['prompt']
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