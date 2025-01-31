from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    """Admin panelda foydalanuvchilarni boshqarish"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("pk", "first_name", "last_name", "phone_number", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Shaxsiy ma’lumotlar", {"fields": ("first_name", "last_name", "avatar")}),
        ("Ruxsatlar", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Tizim ma’lumotlari", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "first_name", "last_name", "avatar", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, CustomUserAdmin)
