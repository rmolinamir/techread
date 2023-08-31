from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as t
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "_id",
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["_id", "id", "email"]

    list_filter = ["email", "is_staff", "is_active"]

    fieldsets = (
        (t("Login Credentials"), {"fields": ("email", "password")}),
        (t("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            t("Permissions & Groups"),
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (t("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            t("Login Credentials"),
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (
            t("Personal Info"),
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name"),
            },
        ),
    )

    search_fields = ["email", "first_name", "last_name"]


admin.site.register(User, UserAdmin)
