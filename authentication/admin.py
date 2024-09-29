from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from authentication.models import *
from django.contrib.auth.admin import UserAdmin as OriginalAdmin


class UserAdmin(OriginalAdmin):

    list_display = (
        "username",
        "email",
        "user_type",
        "date_joined",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "user_type")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ("date_joined", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")


admin.site.register(AuthUser, UserAdmin)
