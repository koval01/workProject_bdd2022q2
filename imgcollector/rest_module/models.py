from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CUSTOMER_TYPE = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    customer_type = models.CharField(
        default='basic', choices=CUSTOMER_TYPE, null=False, max_length=16)
