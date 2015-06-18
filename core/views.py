import json
import logging
from datetime import datetime

from google.appengine.api import (
    urlfetch,
    memcache,
    users,
)
from google.appengine.ext import deferred

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djangae.utils import on_production

from core.lottery import pick_bugmans, WEEK_DAYS
from core.dummy import PROJECTS, USERS, ALLOCATIONS
from core.models import LotteryResult

ALLIGATOR_URL_PATTERN = 'https://potato-alligator-v2.appspot.com/api/v2/%s/?format=json'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


ALLIGATOR_PROJECTS = 'projects'
ALLIGATOR_USERS = 'users'
ALLIGATOR_ALLOCATIONS = 'allocations'
CACHE_TIME = 60 * 60 * 6


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


def get_data(endpoint, refresh=False):
    data = memcache.get(endpoint)
    if not refresh and data:
        return data

    response = urlfetch.fetch(
        ALLIGATOR_URL_PATTERN % endpoint,
        method='GET',
        follow_redirects=False,
        deadline=60,
        validate_certificate=False,
        headers={
            'X-Appengine-Cron': True
        }
    )
    data = json.loads(response.content)

    spt = datetime.strptime
    now = datetime.now()

    lambdas = {
        ALLIGATOR_PROJECTS: lambda x: x['name'] not in ['', None],
        ALLIGATOR_USERS: lambda x: x['role'] in ["FE", "BE", "AR"],
        ALLIGATOR_ALLOCATIONS: lambda x: x['user'] is not None and spt(x['start'], DATETIME_FORMAT) < now < spt(x['end'], DATETIME_FORMAT)
    }
    data = filter(lambdas[endpoint], data)
    memcache.set(endpoint, data, time=CACHE_TIME)
    return data


def get_user_projects(username):
    projects = get_data(ALLIGATOR_PROJECTS)
    allocations = get_data(ALLIGATOR_ALLOCATIONS)
    allocated_projects = [p['project'] for p in filter(lambda usr: usr['user'] == username, allocations)]
    return filter(lambda x: x['id'] in allocated_projects, projects)


def get_username():
    return users.get_current_user().email().split('@')[0]


def alligator(request):

    flush_cache = bool(request.GET.get('flush', False))
    if flush_cache:
        memcache.flush_all()

    if on_production():
        projects = get_user_projects(get_username())
        users = get_data(ALLIGATOR_USERS)
        user_names = map(lambda usr: usr['username'], users)
        allocations = filter(lambda usr: usr['user'] in user_names, get_data(ALLIGATOR_ALLOCATIONS))
    else:
        projects = PROJECTS
        users = USERS
        allocations = ALLOCATIONS

    projects = sorted(projects, key=lambda p: p['name'].lower())

    data = {
        ALLIGATOR_PROJECTS: projects,
        ALLIGATOR_USERS: users,
        ALLIGATOR_ALLOCATIONS: allocations,
    }
    return HttpResponse(json.dumps(data))


def alligator_data_refresh(request):
    for endpoint in [ALLIGATOR_USERS, ALLIGATOR_PROJECTS, ALLIGATOR_ALLOCATIONS]:
        logging.info("Refreshing %s" % endpoint)
        deferred.defer(get_data, endpoint, refresh=True)
    return HttpResponse('Data refreshed!')
