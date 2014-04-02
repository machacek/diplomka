from django.views.generic import TemplateView, DetailView, ListView
from django.db.models import Count
from ranks.models import RankProject, Segment
#from django.shortcuts import render

# Create your views here.

class ProjectListView(ListView):
    model = RankProject
    template_name = "ranks/project_list.html"

class AnnotateView(TemplateView):
    template_name = "ranks/annotate.html"
    
    def get_sentence(self):
        sentence = Segment.objects\
                .filter(sentence__project__pk = self.kwargs['pk'])\
                .annotate(num_annot=Count('annotations'))\
                .order_by('-num_annot')\
                .first()\
                .sentence

        return sentence

    def get_context_data(self, *args, **kwargs):
        context = super(AnnotateView, self).get_context_data(**kwargs)
        sentence = self.get_sentence()
        context['sentence'] = sentence

        segment = sentence.segments.all().first()
        context['candidates_str'] = segment.candidates_str.split('\n')


        return context
