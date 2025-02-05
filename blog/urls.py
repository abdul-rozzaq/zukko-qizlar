from django.urls import path

from .views import BookDetailPageView, BooksPageView, HomePageView, QuotesPageView, ReviewsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("books/", BooksPageView.as_view(), name="books"),
    path("books/<int:pk>/", BookDetailPageView.as_view(), name="book-detail"),
    path("reviews/", ReviewsPageView.as_view(), name="reviews"),
    path("quotes/", QuotesPageView.as_view(), name="quotes"),
]
