from django.db import models
from .user import User
from .company import Company
from .base import BaseModel

# Create your models here.

class UserPrivacyModelPrompt(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField(null=True)
