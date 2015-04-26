import json

from django.views.generic import TemplateView
from django.http import HttpResponse

from lottery import pick_bugmans


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


def bugmans(request, project_id):
    devs = ['user1', 'user2', 'user3', 'user4', 'user5']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    losers = pick_bugmans(devs, days)
    return HttpResponse(json.dumps(losers))
