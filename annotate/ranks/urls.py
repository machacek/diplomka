from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ranks.views import ProjectListView, AnnotateView

urlpatterns = patterns('',
    url(r'^projects/$', ProjectListView.as_view(), name="ranks.views.projectlistview"),
    # url(r'^projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name="s.views.projectdetailview"),
    url(r'^projects/(?P<pk>\d+)/annotate/$', AnnotateView.as_view(), name="ranks.views.annotateview"),
)
