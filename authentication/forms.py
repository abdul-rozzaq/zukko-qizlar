from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """Foydalanuvchi ro‘yxatdan o‘tish formasi"""

    class Meta:
        model = User
        fields = ("phone_number", "full_name", "email", "avatar")

class CustomUserChangeForm(UserChangeForm):
    """Foydalanuvchi ma’lumotlarini yangilash formasi"""

    class Meta:
        model = User
        fields = ("phone_number", "full_name", "email", "avatar")
