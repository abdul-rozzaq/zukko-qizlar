from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import generic

from .forms import CustomUserChangeForm, CustomUserCreationForm, LoginForm


class LoginView(generic.TemplateView):
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)

                return redirect("home")

            else:
                messages.warning(request, "Parol xato yoki bunday foydalanuvchi mavjud emas")
        else:
            messages.warning(request, "Ma'lumotlar to'ldirishda xatolik")

        return self.get(request)


class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class RegistrationView(generic.TemplateView):
    template_name = "authentication/registration.html"

    def post(self, request, *args, **kwargs):

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! Tizimga kiring.")

            return redirect("login")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            return self.get(request)


class SettingsView(generic.TemplateView):
    template_name = "authentication/settings.html"

    def post(self, request, *args, **kwargs):
        phone_number = request.user.phone_number

        post_data = request.POST.copy()
        post_data["phone_number"] = phone_number

        form = CustomUserChangeForm(data=post_data, files=request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect("settings")
        else:
            print(form.errors)

        return self.get(request)


class MyReviewsView(generic.TemplateView):
    template_name = "authentication/my-reviews.html"


class MyQuotesView(generic.TemplateView):
    template_name = "authentication/my-quotes.html"
