import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .base_api import BasePublicApi
from new_app.api.jsonResponse import baseHttpResponse

class PublicApi(BasePublicApi):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = baseHttpResponse()
        return JsonResponse(response.dict(), safe=False)

    def post(self, request, format=None):
        return JsonResponse({
            'err': 0,
            'errMessage': '',
        }, safe=False)