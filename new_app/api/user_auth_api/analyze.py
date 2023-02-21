from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

import os

class AnalyzeApi(BaseUserAuthApi):
    def post(self, request, *args, **kwargs):
        response = baseHttpResponse()
        file_path = request.data['file_path']
        # print('file_path', file_path)
        # print(os.path.exists(file_path))
        try:
            text = open(os.path.join(file_path), 'rb').read()
            response.message = f"start to analyze"
        except:
            response.err = 1
            response.errMessage = f"cant load file path"

        return JsonResponse(response.dict())