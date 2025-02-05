from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import generic

from blog.models import Book, Quote, Review

from .forms import CustomUserChangeForm, CustomUserCreationForm, LoginForm, QuoteForm, ReviewForm


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

            login(request=request, user=user)

            return redirect("registration-complete")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            return self.get(request)


class RegistrationCompleteView(generic.TemplateView):
    template_name = "authentication/registration-complete.html"


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


class MyReviewsView(generic.ListView):
    template_name = "authentication/my-reviews.html"
    queryset = Review.objects.all()

    def get_queryset(self):
        return self.queryset.filter(writer=self.request.user)


class MyQuotesView(generic.ListView):
    template_name = "authentication/my-quotes.html"
    queryset = Quote.objects.all()

    def get_queryset(self):
        return self.queryset.filter(writer=self.request.user).order_by("-pk")


class MyBooksView(generic.TemplateView):
    template_name = "authentication/my-books.html"


class AddQuotePageView(generic.TemplateView):
    template_name = "authentication/add-quote.html"

    def post(self, request, *args, **kwargs):

        form = QuoteForm(request.POST)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.writer = request.user

            quote.save()

            return redirect("my-quotes")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

        return self.get(request)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["books"] = Book.objects.all()

        return data


class AddReviewPageView(generic.TemplateView):
    template_name = "authentication/add-review.html"

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = ReviewForm(request.POST)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.writer = request.user

            quote.save()

            return redirect("my-reviews")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

        return self.get(request)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["books"] = Book.objects.all()

        return data
