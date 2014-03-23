from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ranks.views import AnnotateView

urlpatterns = patterns('',
    url(r'^$', AnnotateView.as_view())
)
