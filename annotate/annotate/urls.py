from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from annotate.views import AboutView

import ranks.urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ranks/', include(ranks.urls)),
    url(r'^about/', AboutView.as_view()),
)
