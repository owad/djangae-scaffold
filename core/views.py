import json
import logging
from datetime import datetime

from google.appengine.api import urlfetch
from google.appengine.api import memcache

from django.views.generic import TemplateView, CreateView
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from djangae.utils import on_production

from core.lottery import pick_bugmans, WEEK_DAYS
from core.dummy import PROJECTS, USERS, ALLOCATIONS
from core.models import LotteryResult

ALLIGATOR_URL_PATTERN = 'https://potato-alligator-v2.appspot.com/api/v2/%s/?format=json'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


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
        logging.warning('%s from cache' % endpoint)
        return data

    response = urlfetch.fetch(
        ALLIGATOR_URL_PATTERN % endpoint,
        method='GET',
        follow_redirects=False,
        deadline=60,
        validate_certificate=False,
    )
    data = json.loads(response.content)

    spt = datetime.strptime
    now = datetime.now()

    lambdas = {
        'projects':lambda x: x['name'] not in ['', None],
        'users': None,
        'allocations': lambda x: x['user'] != None and spt(x['start'], DATETIME_FORMAT) < now < spt(x['end'], DATETIME_FORMAT)
    }
    data = filter(lambdas[endpoint], data)
    memcache.set(endpoint, data, time=60*60*24)
    logging.warning('%s refreshed' % endpoint)
    return data


def get_user_projects(username):
    projects = get_data('projects')
    allocations = get_data('allocations')
    allocated_projects = [p['project'] for p in filter(lambda x: x['user'] == username, allocations)]
    user_projects = filter(lambda x: x['id'] in allocated_projects, projects)
    return user_projects


def alligator(request):

    flush_cache = bool(request.GET.get('flush', False))
    if flush_cache:
        memcache.flush_all()

    if on_production():
        projects = get_user_projects(request.gae_username)
        users = get_data('users')
        allocations = get_data('allocations')
    else:
        projects = PROJECTS
        users = USERS
        allocations = ALLOCATIONS

    projects = sorted(projects, key=lambda p: p['name'].lower())

    data = {
        'projects': projects,
        'users': users,
        'allocations': allocations,
    }
    return HttpResponse(json.dumps(data))
