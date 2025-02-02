from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    first_name = models.CharField(_("Ism"), max_length=150, blank=False)
    last_name = models.CharField(_("Familiya"), max_length=150, blank=False)

    image = models.ImageField(_("Rasmi"), upload_to="avatars/", default="authors/default.png")

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Yozuvchi"), null=True, blank=True)
    name = models.CharField(_("Nomi"), max_length=256)
    description = models.TextField(_("Haqida"))
    published_date = models.DateField(_("Chiqarilgan sana"))
    image = models.ImageField(_("Rasmi"), upload_to="books/", default="books/default.png")
    page_count = models.IntegerField(_("Sahifalar soni"), default=0)

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name
