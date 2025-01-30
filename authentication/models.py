from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None):
        if not phone_number:
            raise ValueError("Telefon raqami kiritilishi shart")

        user = self.model(phone_number=phone_number, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None):
        """Superuser yaratish"""
        user = self.create_user(phone_number, full_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_("Telefon raqam"))
    full_name = models.CharField(max_length=255, verbose_name=_("To‘liq ism"))
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", verbose_name=_("Avatar"))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.full_name
