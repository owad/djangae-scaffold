from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^bugmans/(?P<project_id>[0-9]+)/$', views.bugmans, name='bugmans'),
)