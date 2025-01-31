from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Foydalanuvchi ro‘yxatdan o‘tish formasi"""

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "avatar")

        error_messages = {
            "phone_number": {
                "unique": "Bu telefon raqami bilan allaqachon ro‘yxatdan o‘tilgan!",
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar bir xil emas!")

        if len(password2.strip()) <= 7:
            raise forms.ValidationError("Parol juda qisqa. Eng kamida 8 ta belgidan iborat bo'lishi kerak!")

        return password2


class CustomUserChangeForm(UserChangeForm):
    """Foydalanuvchi ma’lumotlarini yangilash formasi"""

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name", "avatar")


class LoginForm(forms.Form):
    phone_number = forms.CharField(min_length=10)
    password = forms.CharField()

    def get_user(self):
        phone_number = self.cleaned_data.get("phone_number")
        password = self.cleaned_data.get("password")

        user = User.objects.filter(phone_number=phone_number).first()

        if user and user.check_password(password):
            return user

        return None
