from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, UserConfirmation, PasswordReset

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff']
    
    fieldsets = (
    (None, {"fields": ("username", "password")}),
    (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
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

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    pass

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    pass