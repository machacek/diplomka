from django.views.generic import TemplateView
#from django.shortcuts import render

# Create your views here.

class AnnotateView(TemplateView):
    template_name = "ranks/annotate.html"

