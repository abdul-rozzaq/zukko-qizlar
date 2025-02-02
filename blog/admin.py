from django.contrib import admin

from .models import Author, Book


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["pk", "first_name", "last_name", "image"]
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "description", "author", "image"]
