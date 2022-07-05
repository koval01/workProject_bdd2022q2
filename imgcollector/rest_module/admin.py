from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'customer_type'
    )
    list_filter = ('is_staff', 'customer_type')


admin.site.register(CustomUser, CustomUserAdmin)
