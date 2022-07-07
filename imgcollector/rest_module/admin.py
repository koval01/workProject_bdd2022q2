from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from .models import Photo, CustomUser as User
import json
import logging

logger = logging.getLogger(__name__)


class UserDjangoAdmin(UserAdmin):
    readonly_fields = ("is_superuser",)
    list_display = (
        "email", "username", "is_staff", "is_active",
        "last_login", "customer_type")
    list_filter = (
        "is_active", "is_staff", "is_superuser", "customer_type")
    fieldsets = UserAdmin.fieldsets + (
        ("Customer", {'fields': ('customer_type',)}),
    )
    search_fields = (
        "email", "username", "first_name", "last_name")

    list_per_page = 15

    def has_delete_permission(self, request, obj=None):
        if obj.is_superuser if obj else None:
            return False
        return True


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ['action_time', 'content_type', 'action_flag']
    fields = [
        'action_time', 'user', 'content_type', 'change_msg',
        'object_repr', 'action_flag', 'object_id'
    ]
    readonly_fields = fields[:]
    search_fields = (
        "action_flag", "user", "content_type", "object_id")
    ordering = ('-action_time',)

    @staticmethod
    def change_msg(instance):
        json_body = json.loads(instance.change_message)
        try:
            return ",\x20".join([
                f.encode("utf-8").decode("utf-8")
                for f in json_body[0][
                    [i[0] for i in json_body[0].items()][0]
                ]["fields"]
            ])
        except Exception as e:
            logger.debug("Error parsing change_message. Details: %s" % e)
            return "N/A"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_per_page = 15


class AdminPhoto(admin.ModelAdmin):
    list_display = ("name", "created_at", "creator")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name", "creator")
    ordering = ("-created_at",)

    list_per_page = 15


admin.site.register(User, UserDjangoAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Photo, AdminPhoto)

admin.site.site_header = 'Project_bdd2022q2'
