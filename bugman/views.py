import json

from django.views.generic import TemplateView
from django.http import HttpResponse

from lottery import pick_bugmans, WEEK_DAYS
from dummy import PROJECTS, USERS, ALLOCATIONS


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


def bugmans(request, project_id):
    devs = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7']
    losers = pick_bugmans(devs, WEEK_DAYS)
    return HttpResponse(json.dumps(losers))


def alligator(request):
    data = {
        'projects': PROJECTS,
        'users': USERS,
        'allocations': ALLOCATIONS
    }
    return HttpResponse(json.dumps(data))