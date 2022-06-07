from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from simple_history.admin import SimpleHistoryAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import LogUserLoginAttempts, User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "mobile_phone", "password", "password_complex")}),
        (
            "Permissions",
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
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                    "password_changed",
                    "account_locked_at",
                )
            },
        ),
        ("Other", {"fields": ("preferred_message_type",)},),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2"),},),
    )
    list_display = ("email", "mobile_phone", "is_staff")
    search_fields = (
        "email",
        "patient__ssid",
    )
    ordering = ("email",)


@admin.register(LogUserLoginAttempts)
class LogUserLoginAttemptsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "id_user",
        "ip_address",
        "was_successful",
        "locked_out",
        "date_time",
    )
    search_fields = ("ip_address", "was_successful", "locked_out", "date_time")
    list_filter = ("was_successful", "locked_out", "date_time")

    def id_user(self, obj):
        return obj.user.id
