from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    CUSTOMER_TYPE = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    customer_type = models.CharField(default='basic', choices=CUSTOMER_TYPE, null=False, max_length=16)
