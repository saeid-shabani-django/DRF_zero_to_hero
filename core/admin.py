from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, AdminUserCreationForm

from core.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email", "usable_password", "password1", "password2"),
            },
        ),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    


