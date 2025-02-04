from django.shortcuts import render
from django.views import generic


class HomePageView(generic.TemplateView):
    template_name = "index.html"
    template_name_unauthorized = "unauthorized.html"

    def get_template_names(self):
        return [self.template_name if self.request.user.is_authenticated else self.template_name_unauthorized]


class BooksPageView(generic.TemplateView):
    template_name = "books.html"


class QuotesPageView(generic.TemplateView):
    template_name = "quotes.html"


class ReviewsPageView(generic.TemplateView):
    template_name = "reviews.html"
