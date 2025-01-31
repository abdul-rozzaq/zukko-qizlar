from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None):
        if not phone_number:
            raise ValueError("Telefon raqami kiritilishi shart")

        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password=None):
        """Superuser yaratish"""
        user = self.create_user(phone_number, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("Ism"), max_length=150, blank=False)
    last_name = models.CharField(_("Familiya"), max_length=150, blank=False)

    phone_number = models.CharField(max_length=15, unique=True, verbose_name=_("Telefon raqam"))
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", verbose_name=_("Avatar"))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
