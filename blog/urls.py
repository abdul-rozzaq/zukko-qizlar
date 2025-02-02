from django.urls import path

from .views import BooksPageView, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("books/", BooksPageView.as_view(), name="books"),
]
