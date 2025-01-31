from django.urls import path

from .views import LoginView, LogoutView, RegistrationView, SettingsView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="register"),
    #
    path("logout/", LogoutView.as_view(), name="logout"),
    #
    path("settings/", SettingsView.as_view(), name="settings"),
    path("my-reviews/", RegistrationView.as_view(), name="my-reviews"),
    path("my-quotes/", RegistrationView.as_view(), name="my-quotes"),
]
