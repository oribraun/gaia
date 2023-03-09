from django.db import models
from .user import User
from .base import BaseModel

# Create your models here.

class UserSetting(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(default='', max_length=100)
    data = models.JSONField(default=dict, null=True)

    class Meta:
        unique_together = ('user', 'key',)
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'key', ]),
        ]
