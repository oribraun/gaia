from django.db import models
import binascii
import os
from new_app.current_user import get_current_user
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .company import Company

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(BaseModel, AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    TRAIL = 1
    BASIC = 2
    ADVANCE =3
    PRO =3

    ROLE_CHOICES = (
        (TRAIL, 'Trail'),
        (BASIC, 'Basic'),
        (ADVANCE, 'Advance'),
        (PRO, 'Pro'),
    )

    email = models.EmailField(_("email address"), blank=True, unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default=TRAIL)
    password_reset_timestamp = models.DateTimeField(null=True, blank=True)
    api_total_requests = models.IntegerField(null=False, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    gaia_admin = models.BooleanField(default=False)
    # created_by = models.ForeignKey('auth.User', default=get_current_user)