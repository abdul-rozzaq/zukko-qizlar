from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    """Admin panelda foydalanuvchilarni boshqarish"""
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    list_display = ("phone_number", "full_name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Shaxsiy ma’lumotlar", {"fields": ("full_name", "email", "avatar")}),
        ("Ruxsatlar", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Tizim ma’lumotlari", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "full_name", "email", "avatar", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("phone_number", "full_name", "email")
    ordering = ("phone_number",)
    filter_horizontal = ("groups", "user_permissions")

admin.site.register(User, CustomUserAdmin)
