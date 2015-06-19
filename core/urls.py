from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^bugmans/(?P<project_id>[0-9]+)/$', views.bugmans, name='bugmans'),
    url(r'^api/alligator/$', views.alligator, name='alligator'),

    url(r'^_ah/cron/alligator/$', views.alligator_data_refresh, name='alligator_refresh'),
)
