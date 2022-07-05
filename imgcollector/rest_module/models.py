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


class Photo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photo/%Y/%m/%d/', null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='movies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
