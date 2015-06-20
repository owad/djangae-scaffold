import json
import logging
from datetime import datetime
from copy import copy

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

POTATO_ROLES = ["FE", "BE", "AR"]  # only there potatoes will be included in the lottery


class Home(TemplateView):
    template_name = 'bugman/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(Home, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

home = Home.as_view()


@csrf_exempt
def bugmans(request, project_id):
    """
    Returns current week's results for a selected projects in a JSON format
    """

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
    """
    Retrieves alligator data and caches it if needed
    """

    data = memcache.get(endpoint)
    logging.warning(["Refresh: ", refresh, "Data: ", bool(data)])
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
    memcache.set(endpoint, data, time=CACHE_TIME)
    return data


def get_filtered_data(endpoint):
    """
    Cleans and filters alligator data
    """

    data = get_data(endpoint)
    spt = datetime.strptime
    now = datetime.now()

    lambdas = {
        ALLIGATOR_PROJECTS: lambda x: x['name'] not in ['', None],
        ALLIGATOR_USERS: lambda x: x['role'] in POTATO_ROLES,
        ALLIGATOR_ALLOCATIONS: lambda x: x['user'] is not None and spt(x['start'], DATETIME_FORMAT) < now < spt(x['end'], DATETIME_FORMAT)
    }
    return filter(lambdas[endpoint], data)


def get_user_projects(username):
    projects = get_filtered_data(ALLIGATOR_PROJECTS)
    allocations = get_filtered_data(ALLIGATOR_ALLOCATIONS)
    allocated_projects = [p['project'] for p in filter(lambda usr: usr['user'] == username, allocations)]
    return filter(lambda x: x['id'] in allocated_projects, projects)


def alligator(request):
    """
    Returns JSON data retrieved from the alligator app
    """

    if on_production():
        projects = get_user_projects(request.gae_username)
        users = get_filtered_data(ALLIGATOR_USERS)
        all_users = get_data(ALLIGATOR_USERS)
        user_names = map(lambda usr: usr['username'], users)
        allocations = filter(lambda usr: usr['user'] in user_names, get_filtered_data(ALLIGATOR_ALLOCATIONS))
    else:
        projects = PROJECTS
        users = USERS
        all_users = USERS
        allocations = ALLOCATIONS

    projects = sorted(projects, key=lambda p: p['name'].lower())

    data = {
        ALLIGATOR_PROJECTS: projects,
        ALLIGATOR_USERS: users,
        ALLIGATOR_ALLOCATIONS: allocations,
        'all_users': all_users,
    }
    return HttpResponse(json.dumps(data))


def alligator_data_refresh(request):
    for endpoint in [ALLIGATOR_USERS, ALLIGATOR_PROJECTS, ALLIGATOR_ALLOCATIONS]:
        logging.info("Refreshing %s" % endpoint)
        deferred.defer(get_data, endpoint, refresh=True)
    return HttpResponse('Data refreshed!')
