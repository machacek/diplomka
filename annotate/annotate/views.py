from django.views.generic import TemplateView
#from django.shortcuts import render

# Create your views here.

class AboutView(TemplateView):
    template_name = "annotate/about.html"

