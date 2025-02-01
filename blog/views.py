from django.shortcuts import render
from django.views import generic


class HomePageView(generic.TemplateView):
    template_name = "index.html"
    template_name_unauthorized = "unauthorized.html"

    def get_template_names(self):
        return [self.template_name if self.request.user.is_authenticated else self.template_name_unauthorized]
