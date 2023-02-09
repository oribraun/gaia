from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
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
      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default=TRAIL)
      password_reset_timestamp = models.DateTimeField(null=True, blank=True)
      api_total_requests = models.IntegerField(null=False, blank=True, default=0)


class ExampleModel(models.Model):
	firstname    = models.CharField(max_length=200)
	lastname     = models.CharField(max_length=200)
