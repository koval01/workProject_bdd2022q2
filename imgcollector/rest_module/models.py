from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUser(User):
    CUSTOMER_TYPE = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    customer_type = models.CharField(default='basic', choices=CUSTOMER_TYPE, null=False, max_length=16)
