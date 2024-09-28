from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from authentication.models import *

admin.site.site_header = 'DSAPTEA Financial Management System'
admin.site.index_title = 'Dashboard'
admin.site.site_title = 'DSAPTEA Financial Management System'

class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'date_joined', 'last_login')
    fieldsets = (
        (None, {"fields": ("username", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_type",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(AuthUser, UserAdmin)