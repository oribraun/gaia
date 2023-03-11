from django.db import models
import binascii
import os
from .base import BaseModel

# Create your models here.
class Company(BaseModel):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, unique=True, default=None, null=True)
    key = models.CharField(max_length=60, unique=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['domain']),
        ]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Company, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(30)).decode()

    def __str__(self):
        return self.name
#
# class CompanyTokens(Main):
#     key = models.CharField(max_length=40, unique=True)
#     company: Company = models.OneToOneField(
#         Company, related_name='auth_token',
#         on_delete=models.CASCADE, verbose_name="Company"
#     )
#
#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super(CompanyTokens, self).save(*args, **kwargs)
#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()
#
#     def __str__(self):
#         return self.key