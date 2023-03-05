from django.db import models
from .user import User
from .company import Company
from .base import BaseModel

# Create your models here.

class CompanyAdmin(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('user', 'company',)