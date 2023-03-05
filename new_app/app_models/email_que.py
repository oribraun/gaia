from django.db import models
import binascii
import os
from .base import BaseModel

# Create your models here.
class EmailQue(BaseModel):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sender = models.CharField(max_length=200)
    recipient_list = models.JSONField(default=list)
    sent = models.BooleanField(default=False)