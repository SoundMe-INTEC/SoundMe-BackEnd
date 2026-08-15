from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("identification", "email", "identification_type", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "identification_type")
    search_fields = ("identification", "email", "phone")
    ordering = ("identification",)
    fieldsets = (
        (None, {"fields": ("identification", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone")}),
        ("Permissions", {"fields": ("identification_type", "role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "identification",
                    "email",
                    "password1",
                    "password2",
                    "identification_type",
                    "role",
                    "phone",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
