from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import User


class Author(models.Model):
    first_name = models.CharField(_("Ism"), max_length=150, blank=False)
    last_name = models.CharField(_("Familiya"), max_length=150, blank=False)

    image = models.ImageField(_("Rasmi"), upload_to="avatars/", default="authors/default.png")

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Yozuvchi"), null=True, blank=True)
    name = models.CharField(_("Nomi"), max_length=256)
    description = models.TextField(_("Haqida"))
    published_date = models.DateField(_("Chiqarilgan sana"))
    image = models.ImageField(_("Rasmi"), upload_to="books/", default="books/default.png")
    page_count = models.IntegerField(_("Sahifalar soni"), default=0)

    is_published = models.BooleanField(default=False)

    @property
    def rate(self):
        return float(3) + 0.56

    def __str__(self):
        return self.name


class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("Yozuvchi"))
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name=_("Kitob"))

    body = models.TextField(verbose_name=_("Matn"))
    rate = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("Yozuvchi"))
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True, blank=True)

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
