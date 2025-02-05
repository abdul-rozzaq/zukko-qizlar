from django.urls import path

from .views import AddQuotePageView, LoginView, LogoutView, MyBooksView, MyQuotesView, MyReviewsView, RegistrationCompleteView, RegistrationView, SettingsView, AddReviewPageView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="register"),
    path("registration-complete/", RegistrationCompleteView.as_view(), name="registration-complete"),
    #
    path("logout/", LogoutView.as_view(), name="logout"),
    #
    path("settings/", SettingsView.as_view(), name="settings"),
    path("my-reviews/", MyReviewsView.as_view(), name="my-reviews"),
    path("my-quotes/", MyQuotesView.as_view(), name="my-quotes"),
    path("my-books/", MyBooksView.as_view(), name="my-books"),
    path("add-quote/", AddQuotePageView.as_view(), name="add-quote"),
    path("add-review/", AddReviewPageView.as_view(), name="add-review"),
]
