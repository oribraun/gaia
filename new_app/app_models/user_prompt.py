from django.db import models
from .user import User
from .base import BaseModel

# Create your models here.

class UserPrompt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    ip_address = models.GenericIPAddressField(null=True)
