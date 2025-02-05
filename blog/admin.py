from django.contrib import admin

from .models import Author, Book, Quote, Review


class BookInline(admin.StackedInline):
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["pk", "first_name", "last_name", "image"]
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "description", "author", "image"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["pk", "writer", "book", "rate", "created_at"]
    list_editable = ["rate"]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ["pk", "writer", "book"]
