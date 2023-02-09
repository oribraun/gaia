from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .base_api import BaseUserAuthApi
from new_app.api.jsonResponse import baseHttpResponse

import os

class UploadFileApi(BaseUserAuthApi):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
        # print('path', path)
        # text = open(os.path.join(settings.MEDIA_ROOT, 'uploads/Activation Code.txt'), 'rb').read()
        # print('text', text)
        dirs = os.path.dirname(path)
        if not os.path.exists(dirs):
            os.makedirs(os.path.dirname(path))
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        response = baseHttpResponse()
        response.file_path = f"{settings.MEDIA_ROOT}uploads/{file.name}"
        return JsonResponse(response.dict())