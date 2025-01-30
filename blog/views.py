from django.shortcuts import render
from django.views import generic


class HomePageView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["name"] = "SSSSSSSSSS"

        return data
