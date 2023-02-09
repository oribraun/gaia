from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

import os

class AnalyzeApi(BaseUserAuthApi):
    def post(self, request, *args, **kwargs):
        file_path = request.data['file_path']
        print(os.path.exists(file_path))
        text = open(os.path.join(file_path), 'rb').read()
        # print('text', text)
        print('file_path', file_path)
        response = baseHttpResponse()
        response.message = f"start to analyze"
        return JsonResponse(response.dict())