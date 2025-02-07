from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from .filters import BookFilter
from .models import Author, Book, Quote, Review, User


class HomePageView(generic.TemplateView):
    template_name = "index.html"
    template_name_unauthorized = "unauthorized.html"

    def get_template_names(self):
        return [self.template_name if self.request.user.is_authenticated else self.template_name_unauthorized]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["last_reviews"] = Review.objects.order_by("pk")[:2]
        data["following_reviews"] = Review.objects.all()
        data["recomended_books"] = Book.objects.all().order_by('?')[:6]

        return data


class BooksPageView(generic.ListView):
    template_name = "books.html"
    queryset = Book.objects.all()

    def get_queryset(self):

        query = self.request.GET.get("query")

        if not query:
            return self.queryset.all()

        return self.queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))


class BookDetailPageView(generic.DetailView):
    queryset = Book.objects.all()
    template_name = "book-detail.html"


class QuotesPageView(generic.ListView):
    template_name = "quotes.html"
    queryset = Quote.objects.all()


class ReviewsPageView(generic.ListView):
    template_name = "reviews.html"
    queryset = Review.objects.all()
