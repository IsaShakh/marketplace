from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext as _
# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    exclude = ('username',)
    list_display = ("email", "first_name", "second_name", "is_staff")
    search_fields = ("first_name", "second_name", "email")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": (
            "email",
            "email_verified",
            "phone",
            "birthday",
        )}),
        (_("Personal info"), {"fields": (
            "first_name",
            "second_name",
        )}),
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