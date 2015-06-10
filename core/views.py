import json

from google.appengine.api import urlfetch
from google.appengine.api import memcache

from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from core.lottery import pick_bugmans, WEEK_DAYS
from core.dummy import PROJECTS, USERS, ALLOCATIONS
from core.models import LotteryResult

ALLIGATOR_URL_PATTERN = 'https://potato-alligator-v2.appspot.com/api/v2/%s/?format=json'


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


@csrf_exempt
def bugmans(request, project_id):

    if request.method == 'POST':
        usernames = json.loads(request.body)
        result = pick_bugmans(usernames, WEEK_DAYS)

        # store the result
        LotteryResult.objects.create(
            ran_by=request.user.email.split('@')[0],
            partakers=json.loads(request.body),
            result=[d[1] for d in result],
            project_id=int(project_id),
        )

        return HttpResponse(json.dumps(dict(result)))


def get_data(endpoint):
    data = memcache.get(endpoint)

    if data:
        return data

    response = urlfetch.fetch(
        ALLIGATOR_URL_PATTERN % endpoint,
        method='GET',
        follow_redirects=False,
        deadline=60,
        validate_certificate=False,
    )
    data = json.loads(response.content)

    lambdas = {
        'projects':lambda x: x['project_id'] != None,
        'users': None,
        'allocations': lambda x: x['user'] != None
    }
    data = filter(lambdas[endpoint], data)
    memcache.set(endpoint, data, time=60*60*24)
    return data


def get_user_projects(username):
    projects = get_data('projects')
    allocations = get_data('allocations')

    allocated_projects = [p['project'] for p in filter(lambda x: x['user'] == username, allocations)]
    user_projects = filter(lambda x: x['project_id'] in allocated_projects, projects)
    import logging
    logging.warning(allocations)
    logging.warning(projects)
    logging.warning('==='*20)
    logging.warning(allocated_projects)
    logging.warning(user_projects)
    return user_projects

def alligator(request):
    get_user_projects(request.gae_username)
    projects = get_data('projects')
    users = get_data('users')
    allocations = get_data('allocations')

    data = {
        'projects': projects,
        'users': users,
        'allocations': allocations,
    }
    return HttpResponse(json.dumps(data))
