from django.db import models
from django.urls import resolve
from .base import BaseModel
from .user import User

class UserActivity(BaseModel):
    SUCCESS, FAILED = "Success", "Failed"
    ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(default='', max_length=30)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict, null=True)
    ip_address = models.GenericIPAddressField(null=True)

    @staticmethod
    def create_message(request, user, status_code, data: dict = None):
        action_type = request.path_info
        try:
            action_type = resolve(action_type).route.split('/<', 1)[0].split('$', 1)[0].rsplit('/', 1)[-1]
        except:
            pass
        data = {
            "user": user,
            "action_type": action_type,
            "status": status_code,
            "data": data,
            "ip_address": UserActivity.get_client_ip(request),
        }
        UserActivity.objects.create(**data)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
